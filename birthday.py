from main import BaseHandler
import webapp2
import datetime
now = datetime.datetime.now()

class Birthday_Form(BaseHandler):

     def get(self):
        self.render("birthday.html")
    
     def post(self):

        calender = {'January' : 31, 'February' : 29, 'March': 31, 'April': 30,'May':31,'June':30,'July':31,'August':31,'September':30,'October':31,'November':30,'December':31}

        month = self.request.get("month")
        day = self.request.get("day")

        if day:
            day = int(day)

        year = self.request.get("year")
        
        if year:
            year = int(year)

        submitted_date = 'You submitted: ' + str(month) + ' ' + str(day) + ', ' + str(year)

        if year in range(1900,now.year + 1):
           
           days_in_month = calender.get(month)
           
           if days_in_month < day:
                
                invalid = "Invalid"
                message = 'Date submitted does not exist, there can only be ' + str(days_in_month) + ' days in ' + str(month)
                self.render("birthday.html",month = month, day = day, year = year , submitted_date = submitted_date, message = message, invalid = invalid)
           else:
                valid = 'Valid'
                self.render("birthday.html",month = month, day = day, year = year , submitted_date = submitted_date, valid = valid)

        else:
            
            error = 'You must enter a year between 1900 and ' + str(now.year)
            self.render("birthday.html", error = error, month = month, day = day)

app = webapp2.WSGIApplication([('/course_work/unit2/birthday', Birthday_Form)
], debug=True)