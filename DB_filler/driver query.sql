with cte_datum as (
	select
		datum::date
	from
		generate_series(now()::date - '18 day'::interval, now(), '1 day'::interval) datum
	
)
,	cte_m as (
	select
		datum +
		minuta * '2 minute'::interval minuta,
		random() razina
	from
		cte_datum 
	cross join
		generate_series(0,719,1) minuta
	
)
, cte_mjerenje as (
select
	minuta,
	case when razina < lag(razina) over (order by minuta) then -random()*(1/720.0)
	else random()*(1/720.0) end mjerenje
	
from
	cte_m
)
, cte_final as (
select
	minuta,
	(sum(mjerenje) over (order by minuta))*1000 razina
from
	cte_mjerenje
)
select
	minuta,
	100 * (abs(min(razina) over ()) + razina) / (max(razina) over() + abs(max(razina) over())) razina
from
	cte_final
order by 
	minuta