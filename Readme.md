![time_series_anomaly_detection_cover.png](attachment:time_series_anomaly_detection_cover.png) 

# Data Dictionary:
**Variable** |    **Value**    | **Meaning**
---|---|---
date | datetime | The date of log entry
time | datetime | The time of the day of log entry
path | string | The path the user is on
user id | float | The primary key of log table, indicating each user
ip | string | The user's ip address
name | string | The name of user's cohort
slack | string | The name of the slack chanel that user belongs to
start date| datetime | The start date of the cohort
end date | datetime | The end date of the cohort
program id | datetime | This indicates which program is the user in

# Question:
# <hr style="border-bottom: 10px groove black; margin-top: 1px; margin-bottom: 1px"></hr>
1. Which lesson appears to attract the most traffic consistently across cohorts (per program)?

• Data Science cohorts viewed classification/overview the most.

• Web Development cohorts viewed javascript-i the most.

# <hr style="border-bottom: 10px groove black; margin-top: 1px; margin-bottom: 1px"></hr>

2. Is there a cohort that referred to a lesson significantly more than other cohorts seemed to gloss over?

# <hr style="border-bottom: 10px groove black; margin-top: 1px; margin-bottom: 1px"></hr>

3. Are there students who, when active, hardly access the curriculum? If so, what information do you have about these students?

• 4 users hardly ever accessed the curriculum.

• All 4 users are from Full Stack Java (Web Development) Program. Their information are provided above.
# <hr style="border-bottom: 10px groove black; margin-top: 1px; margin-bottom: 1px"></hr>

4. Is there any suspicious activity, such as users/machines/etc accessing the curriculum who shouldn’t be? Does it appear that any web-scraping is happening? Are there any suspicious IP addresses?

•There is no suspicious IP address. But for those who have a significant amount of IP addresses during their program, their IP addresses appear to be distributed across the United States.
# <hr style="border-bottom: 10px groove black; margin-top: 1px; margin-bottom: 1px"></hr>

5. At some point in 2019, the ability for students and alumni to access both curriculums (web dev to ds, ds to web dev) should have been shut off. Do you see any evidence of that happening? Did it happen before?

• For the Data Science Program there does not appear to be any access to the Web Dev paths

• For Web Development Program appear to be access the whole time
# <hr style="border-bottom: 10px groove black; margin-top: 1px; margin-bottom: 1px"></hr>

6. What topics are grads continuing to reference after graduation and into their jobs (for each program)?

• Most Visited Topics For Full Stack Java Program: HTML, JavaScript, CSS, Java, Appendix

• Most Visited Topics For Data Science Program: Anomaly Detection, mySQL, Classification, Feature Scaling, AL-ML-DL, SQL Database Design
# <hr style="border-bottom: 10px groove black; margin-top: 1px; margin-bottom: 1px"></hr>

7. Which lessons are least accessed? 

•Web Development Program: there are 400+ pages that were accessed only once. 

•Data Science Program: there are 100+ pages that were accessed only once.

# Conclusion:

What're the main thing found in codeup schedule data?

-Data science doesn't visit curriculum as often as web devs do.

-Data science usually only like to visit old curriculum or curriculums to refresh there mindset 

-Web dev visit the same curriculums 3 time more then data science does with there curriculums 

-For wed dev we would've to teach these following curriculum more or in detail(javascript,  html-css,jquery,spring)all of these curriculum has a total number of 68,323 return.

# Recommendations:

-I would recommend that we teach (javascript, html-css,jquery,spring) for wed dev in more detail or add more time for student to get adjusted to the curriculum. 

-I would recommend for data science to freshen up there knowledge of curriculum learned at the being of the course.

-This isn't fully recommend but hopefully one day data science and wed dev could cross train. 
 
# Next step: 

-Next Step would probably be if my recommendations made a inpact on the number of visit or change the highest path 

-Probably take the wed dev program to get there view on that subject.
