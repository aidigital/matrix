-------------------------------------------------------
/* 1. Populate some dummy tables */
drop table if exists #Exposure
drop table if exists #Regions
GO

create table #Regions(Region varchar(max), Counterparty varchar(max))
insert into #Regions values
  ('Region A', 'Counterparty1'),
  ('Region A', 'Counterparty2'),
  ('Region B', 'Counterparty3'),
  ('Region B', 'Counterparty4'),
  ('Region C', 'Counterparty5')

create table #Exposure(Book varchar(max), Instrument varchar(max), Counterparty varchar(max), TransactionID varchar(max), Date DATE, Exposure int);

insert into #Exposure values
   ('Book1', 'Instrument1', 'Counterparty1', 'T1', '2019-01-15', 100000),
   ('Book1', 'Instrument1', 'Counterparty2', 'T2', '2019-02-20', 175500),
   ('Book1', 'Instrument1', 'Counterparty3', 'T3', '2019-03-05', 100000),
   ('Book1', 'Instrument1', 'Counterparty4', 'T4', '2019-04-10', 400000),
   ('Book1', 'Instrument1', 'Counterparty5', 'T5','2019-05-25', 500000),

   ('Book1', 'Instrument2', 'Counterparty1', 'T6', '2019-01-15', 100000),
   ('Book1', 'Instrument2', 'Counterparty2', 'T7', '2019-02-20', 200000),
   ('Book1', 'Instrument2', 'Counterparty3', 'T8', '2019-03-05', 300000),
   ('Book1', 'Instrument2', 'Counterparty1', 'T9', '2019-04-10', 400000),
   ('Book1', 'Instrument2', 'Counterparty2', 'T10', '2019-05-25', 450000),

   ('Book2', 'Instrument3', 'Counterparty1', 'T11', '2019-01-15', 100000),
   ('Book2', 'Instrument3', 'Counterparty2', 'T12', '2019-02-20', 200000),
   ('Book2', 'Instrument3', 'Counterparty3', 'T13', '2019-03-05', 300000),

   ('Book2', 'Instrument1', 'Counterparty1', 'T14', '2019-04-10', 400000),
   ('Book2', 'Instrument2', 'Counterparty2', 'T15', '2019-05-25', 500000),

   ('Book3', 'Instrument1', 'Counterparty1', 'T16', '2019-01-15', 100000),
   ('Book3', 'Instrument1', 'Counterparty2', 'T17', '2019-02-20', 200000),
   ('Book3', 'Instrument1', 'Counterparty3', 'T18', '2019-03-05', 300000)
GO
--select * from #Exposure
--select * from #Regions

-------------------------------------------------------
/* 2. Queries */

/* 1) Sum, Max, Min, Avg by Book, Instrument, Counterparty  */
select e.Book, e.Instrument, e.Counterparty, r.Region,
       sum(e.exposure) as Total, max(e.exposure) as Max, min(e.exposure) as Min, AVG(e.Exposure) as Avg
from #Exposure e
     LEFT JOIN #Regions r ON r.Counterparty = e.Counterparty  -- r.Counterparty is unique, so no duplicates are coming
--where e.Book = 'Book1' and e.Counterparty = 'Counterparty3'
where r.Region = 'Region A'
group by e.Book, e.Instrument, e.Counterparty, r.Region

/* 2) Get the rows containing the maximum Exposure for each Book */
select x.*, y.*
from #Exposure x
	LEFT JOIN (select Book, max(exposure) as MaxExposure
			   from #Exposure
			   group by Book) y ON x.Book = y.Book and x.Exposure = y.MaxExposure
where x.Book = y.Book and x.Exposure = y.MaxExposure
-- we could do INNER JOIN and get rid of the WHERE clause as well

/* 3) Previous Book-Instrument combination, and to the % increase vs previous exposure  */
select e.*,
       previous_exposure.Date as PreviousDate,
	   previous_exposure.Exposure as PreviousExposure,
	   CONVERT( decimal(10, 3), ((e.Exposure-previous_exposure.Exposure)*100.000/previous_exposure.Exposure) ) [Increase by (%)],
	   --CAST( ((e.Exposure-previous_exposure.Exposure)*100.00/previous_exposure.Exposure) as decimal(10,3) ) [Increase by (%)],

	   -- Using LAG() seems simpler, but we need to call the LAG() function for every column we want (and it gets verbose)
	   -- whereas my "OUTER APPLY" approach gives us access to *ALL* the columns.
	   LAG(e.Date, 1) OVER(Partition By e.Book, e.Instrument ORDER BY e.Date) as PreviousDateWithLag,
	   LAG(e.Exposure, 1) OVER(Partition By e.Book, e.Instrument ORDER BY e.Date) as PreviousExposureWithLag

from #Exposure e
OUTER APPLY (select       -- FYI: OUTER APPLY = LEFT JOIN; CROSS APPLY = INNER JOIN
                  top 1 * -- bringing just 1 row means we definitely won't increase the nr of rows
             from #Exposure x
			 where     x.Book = e.Book
			       and x.Instrument = e.Instrument
				   --and x.Counterparty = e.Counterparty
				   and x.Date < e.Date
            ORDER BY x.DATE DESC
			) previous_exposure
ORDER BY e.Book, e.Instrument, e.Date

