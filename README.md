# MA705FinalProject

This repository contains files used in the MA705 dashboard project.

The final dashboard is deployed on Heroku [here](https://ma705-project-cdeorocki.herokuapp.com).

## Dashboard Description

This dashboard explores the number and origin of billionaires globally, over a period of years from 2000 through 2014.

For each year available, each billionaire at that time, is listed within the dataset. Accompanying this information
are details about the billionaires’ net worth in billions, net worth ranking per year, country and global region of
origin, date of birth, gender, whether their wealth was self-made or inherited, industry of operation, and details
about their associated company.

This dashboard prvoides an easy way to explore the data each year and compare visuals of the billionaire variables above.

### Data Sources

I originally found this dataset on [Data Is Plural](https://www.data-is-plural.com/archive/).

The original data has been published by Forbes each year and was collected further by researchers at Peterson Institute
for International Economics. As part of the study, the scholars tried to attain additional information such as wealth
origin, generation of wealth and company notes. The researchers focused on the years 1996, 2001 and 2014.

The updated data by can be found [here](https://www.piie.com/publications/working-papers/origins-superrich-billionaire-characteristics-database?ResearchID=2917).

This dashboard attempts to provide an easy way to explore the data for all years from 2000 through 2014.

### Other Comments

Originally the data included over 17,000 rows. I only used years from 2000 to 2014 and made sure variables were constant across indiviudal billionaires. I merged the billionaire info dataset and all 1996 through 2015 data set and cleaned it in Spyder which yeilded over 13,000 rows of data. Due to the limitations of Heroku, I pared this dataset down to only the top 300 billionaires per years 2000 through 2014. This was discovered very late in the game when I attempted to deploy to Heroku and therefore this data was more manually compiled from a .csv file I saved locally from the cleaned Python dataset I created originally. I then added this data as the df instead and reuploaded this smaller dataset to Heroku.
