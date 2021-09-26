--Data Source : https://github.com/noorch70/PortfolioProjects/blob/main/Nashville%20Housing%20Data%20for%20Data%20Cleaning%20(1).xlsx
--DATACLEANING NASHVILLE HOUSING

--Standardizing date format (removing timestamp from date column in table)

 Select saleDate from DataCleaning..NashvilleHousing

ALTER TABLE DataCleaning..NashvilleHousing
ALTER COLUMN SaleDate Date;

--Filling out null property addresses
---1) On examining the table,it is found that same parcelIDs always delivered to similar addresses therefore by matching the parcelIDs 
---null property addresses are filled.
SELECT parcelID,propertyAddress
FROM DataCleaning..NashvilleHousing
Order by ParcelID

---2)self joining the table on basis of same parcelIDs since all same parcels delivered to same property address
SELECT a.ParcelID,b.parcelID,a.propertyAddress,b.propertyAddress,ISNULL(a.PropertyAddress,b.propertyAddress)
FROM DataCleaning..NashvilleHousing a
join DataCleaning..NashvilleHousing b
on a.ParcelID=b.ParcelID and a.[UniqueID ]<>b.[UniqueID ]
WHERE a.propertyAddress is null

---3) Filling out the empty address

UPDATE a
SET PropertyAddress=ISNULL(a.PropertyAddress,b.propertyAddress)
FROM DataCleaning..NashvilleHousing a
join DataCleaning..NashvilleHousing b
on a.ParcelID=b.ParcelID and a.[UniqueID ]<>b.[UniqueID ]
WHERE
a.propertyAddress is null


---4)Verifying if any null left in propertyAddress column
Select * from DataCleaning..NashvilleHousing
where
PropertyAddress is null



--Breaking out address(propertyAddress and ownerAddress) into indivisual columns (Address ,City ,State)

---1) slecting the required outputs first 

SELECT SUBSTRING(propertyAddress,1,CHARINDEX(',',propertyAddress)) as Address,
SUBSTRING(propertyAddress,CHARINDEX(',',propertyAddress)+1,len(PropertyAddress)) as town
from DataCleaning..NashvilleHousing

---2) Now adding two more columns : PropertySplitAddress and PropertySplitCiy

ALTER TABLE DataCleaning..NashvilleHousing
Add PropertySplitAddress varchar(255);

ALTER TABLE DataCleaning..NashvilleHousing
Add PropertySplitCity varchar(255);

Update DataCleaning..NashvilleHousing
Set PropertySplitAddress=SUBSTRING(propertyAddress,1,CHARINDEX(',',propertyAddress)-1);

Update DataCleaning..NashvilleHousing
Set PropertySplitCity=SUBSTRING(propertyAddress,CHARINDEX(',',propertyAddress)+1,len(PropertyAddress))

---3)Now verifying the PropertyAddress Columns
SELECT PropertySplitAddress,PropertySplitCity
from DataCleaning..NashvilleHousing

---4)Now  examining OwnerAddress columns
Select OwnerAddress from 
DataCleaning..NashvilleHousing

select PARSENAME(REPLACE(OwnerAddress,',','.'),3),
PARSENAME(REPLACE(OwnerAddress,',','.'),2),
PARSENAME(REPLACE(OwnerAddress,',','.'),1)
from DataCleaning..NashvilleHousing

ALTER TABLE DataCleaning..NashvilleHousing
Add OwnerSplitAddress varchar(255);

ALTER TABLE DataCleaning..NashvilleHousing
Add OwnerSplitCity varchar(255);

ALTER TABLE DataCleaning..NashvilleHousing
Add OwnerSplitState varchar(25);

Update DataCleaning..NashvilleHousing
SET OwnerSplitAddress=PARSENAME(REPLACE(OwnerAddress,',','.'),3);
Update DataCleaning..NashvilleHousing
SET OwnerSplitCity=PARSENAME(REPLACE(OwnerAddress,',','.'),2);
Update DataCleaning..NashvilleHousing
SET OwnerSplitState=PARSENAME(REPLACE(OwnerAddress,',','.'),1)

SELECT * FROM DataCleaning..NashvilleHousing

-------change Y and N to yes and No in "sold as vacant"---------------------------

--checking the entries first
SELECT DISTINCT(SoldAsVacant),count(SoldAsVacant)
FROM
DataCleaning..NashvilleHousing
GROUP BY SoldAsVacant
Order by 2


--Now checking required output

SELECT SoldAsVacant,

CASE WHEN SoldAsVacant = 'Y' then 'Yes'
      WHEN SoldAsVacant = 'N' then 'No'
	  ELSE SoldAsVacant
	  END
FROM DataCleaning..NashvilleHousing

--Updating the table now
UPDATE DataCleaning..NashvilleHousing
SET SoldAsVacant=
CASE WHEN SoldAsVacant = 'Y' then 'Yes'
      WHEN SoldAsVacant = 'N' then 'No'
	  ELSE SoldAsVacant
	  END
FROM DataCleaning..NashvilleHousing

--Now checking if chanes are in place
SELECT DISTINCT(SoldAsVacant),count(SoldAsVacant)
FROM
DataCleaning..NashvilleHousing
GROUP BY SoldAsVacant
Order by 2



----------Remove Duplicates----------

WITH row_numCTE AS ( 
SELECT *,
  ROW_NUMBER() 
  OVER ( PARTITION BY ParcelID,
                      PropertyAddress,
					  SalePrice,
					  SaleDate,
					  LegalReference
					  ORDER BY 
					   UniqueID) row_num
FROM DataCleaning..NashvilleHousing
)
--order by ParcelID
DELETE  
FROM
row_numCTE
WHERE
row_num>1


 


 -----------DELETING UNUSED COLUMNS
SELECT *
FROM 
DataCleaning.dbo.NashvilleHousing

ALTER TABLE DataCleaning.dbo.NashvilleHousing
DROP COLUMN PropertyAddress,OwnerAddress,TaxDistrict
