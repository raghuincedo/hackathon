# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 10:25:05 2017

@author: ansh.goel
"""

from dateutil import rrule,relativedelta
import parsedatetime as pdt
import datetime
import timestring
import re

class DateRangeExtractor():

    cal = pdt.Calendar()
    now = datetime.datetime.now()
    def quartersRule(self, year):
        quarters = rrule.rrule(rrule.MONTHLY,
                       bymonth=(1,4,7,10),
                       bysetpos=-1,
                       dtstart=datetime.datetime(year,1,1),
                       count=8)
        return quarters
    
    def text2int (self, textnum, numwords={}):
        if not numwords:
            units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen",
            ]
    
            tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    
            scales = ["hundred", "thousand", "million", "billion", "trillion"]
    
            numwords["and"] = (1, 0)
            for idx, word in enumerate(units):  numwords[word] = (1, idx)
            for idx, word in enumerate(tens):      numwords[word] = (1, idx * 10)
            for idx, word in enumerate(scales): numwords[word] = (10 ** (idx * 3 or 2), 0)
    
        ordinal_words = {'first':1, 'second':2, 'third':3, 'fifth':5, 'eighth':8, 'ninth':9, 'twelfth':12}
        ordinal_endings = [('ieth', 'y'), ('th', '')]
    
        textnum = textnum.replace('-', ' ')
    
        current = result = 0
        curstring = ""
        onnumber = False
        for word in textnum.split():
            if word in ordinal_words:
                scale, increment = (1, ordinal_words[word])
                current = current * scale + increment
                if scale > 100:
                    result += current
                    current = 0
                onnumber = True
            else:
                for ending, replacement in ordinal_endings:
                    if word.endswith(ending):
                        word = "%s%s" % (word[:-len(ending)], replacement)
    
                if word not in numwords:
                    if onnumber:
                        curstring += repr(result + current) + " "
                    curstring += word + " "
                    result = current = 0
                    onnumber = False
                else:
                    scale, increment = numwords[word]
    
                    current = current * scale + increment
                    if scale > 100:
                        result += current
                        current = 0
                    onnumber = True
    
        if onnumber:
            curstring += repr(result + current)
    
        return curstring
    
    def today_yesterday(self,param):
         daterange={}
         if('today' in param):
             daterange['start']=("%s" %self.now).split()[0]
             daterange['end']=("%s" %self.now).split()[0]
             daterange['string']='today'
         elif('yesterday' in param):
             daterange['start']=("%s" %(self.now-datetime.timedelta(days=1))).split()[0]
             daterange['end']=("%s" %(self.now-datetime.timedelta(days=1))).split()[0]
             daterange['string']='yesterday'
         return daterange    
    
    def reduce_year(self,temp_date):
        temp_date-=relativedelta.relativedelta(years=1)
        return temp_date
    def next_phrase_handle(self,param):
        
        daterange={}
        all_match=[]
        all_match_1=re.findall(r'(?ix)(?:next)\s+(?:[a-z\d]+)\s*(?:[a-z\d]*)',param)
        for i,match in enumerate(all_match_1):
            temp1=match.split()
            string=""
            for j,temp2  in enumerate(temp1):
                if j==1:
                    string+="1 "
                string+=temp2+' '
            all_match.append(string)
        for i,match in enumerate(all_match):
            p1=self.cal.parseDT(match, self.now)[0]
            days_difference=(p1-self.now).days+1
            if(days_difference!=0):
                
                daterange['start']=("%s" %self.now).split()[0]
                daterange['end']=("%s" %p1).split()[0]
                daterange['string']=all_match_1[i]
            return daterange
        if 'today' in param or 'yesterday' in param:
            return self.today_yesterday(param)
        if 'next' in param or 'current' in param:
            a=1
        return None
    
    def last_phrase_handle(self,param):
        daterange={}
        
        msg=param.lower()
        all_match=[]
        all_match_1=re.findall(r'(?ix)(?:last|prior|previous|past)\s+(?:[a-z\d]+)\s*(?:[a-z\d]*)',msg)
        for i,match in enumerate(all_match_1):
            temp1=match.split()
            string=""
            for j,temp2  in enumerate(temp1):
                if j==1:
                    string+="1 "
                string+=temp2+' '
            all_match.append(string)
            
        for i,match in enumerate(all_match):
            p1=self.cal.parseDT(match, self.now)[0]
            days_difference=(p1-self.now).days+1
            if(days_difference!=0):
                
                start_datetime="%s" %(self.now-datetime.timedelta(days=days_difference))
                if("month" in match ):
                    #print((p1-self.now))
                    start_datetime="%s" %(self.now-relativedelta.relativedelta(months=(p1.month-self.now.month +(p1.year-self.now.year)*12)))
                daterange['start']=start_datetime.split()[0]
                daterange['end']=("%s" %self.now).split()[0]
                daterange['string']=all_match_1[i]
            return daterange
        return self.next_phrase_handle(msg)
        #msg = "%s" %(self.cal.parseDT(param, self.now)[0])   
        #dateAndTime = msg.split(" ")
        #return dateAndTime[0]
    
    def dateConvertor(self, param):
        
        daterange={}
        
        msg=param.lower()
       
        msg = "%s" %(self.cal.parseDT(msg, self.now)[0])   
        dateAndTime = msg.split("")
        return dateAndTime[0]
    
    def rangeExtractor(self,message):
        
        dateRange = {}
        
        dateOutput= re.findall(
            r"""(?ix)\b(?:(?:\b\d+(?:\.|st|nd|rd|th)*\b|(?:(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*))[\s,.\/-]*){2,3}\b""",
            message.lower())
        print(dateOutput)
        
        if len(dateOutput) > 0: #check validity of mm/dd/yy dates
            
            del_match=[]
            for i,main_match in enumerate(dateOutput):
                match=re.search(r'(?:\d+[\/\\-]+){2}\d+',main_match)
                
                if(match):
                    match=match.group()
                    match=re.split(r'[\/\\-]',match)
                    #dateOutput[i]=match[1]+'/'+match[0]+'/'+match[2]
                    if len(match)!=3:
                        continue
                    match=[int(i) for i in match]
                    try:
                        a=datetime.datetime(day=match[1],month=match[0],year=match[2])
                    except ValueError:
                        del_match.append(main_match)
            for i in del_match:
                dateOutput.remove(i)
                    
            
            if len(dateOutput) == 2:
                dateRange['start'] = self.cal.parseDT(dateOutput[0].strip(),self.now)[0]
                dateRange['end'] = self.cal.parseDT(dateOutput[1].strip(),self.now)[0]
                if (dateRange['start']-self.now).days>0:
                    dateRange['start']=self.reduce_year(dateRange['start'])
                    dateRange['end']=self.reduce_year(dateRange['end'])
                dateRange['start']=("%s" %dateRange['start']).split()[0]
                dateRange['end']=("%s" %dateRange['end']).split()[0]
                dateRange['string']=dateOutput[0]+' '+dateOutput[1]
                return dateRange
        
        # for january type cases
        match=re.search(r'(?ix)(?:for|in)\s+[a-z]*\s*(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s*\d*',message)
        if(match):
            temp_date=self.cal.parseDT(match.group(), self.now)[0]
            match_validity=re.search(r'\d+',match.group())
            if match_validity: # for 0ct 34, oct 92 type cases
                if int(match_validity.group())<1990 and int(match_validity.group())==temp_date.day:
                    if (temp_date-self.now).days>0:
                        temp_date-=relativedelta.relativedelta(years=1)
                    dateRange['start']="%s" %temp_date.date()
                    dateRange['end']="%s" %temp_date.date()
                    dateRange['string']=match.group()
                    return(dateRange)
                elif int(match_validity.group())>1990:
                    dateRange['start']="%s" %temp_date.date()
                    num_days=pdt.calendar.monthrange(temp_date.year, temp_date.month)[1]
                    dateRange['end']=("%s" %(temp_date+datetime.timedelta(num_days-1))).split()[0]
                    dateRange['string']=match.group()
                    return dateRange 
                else:
                    return None
            else:
                if (temp_date-self.now).days>0:
                    temp_date-=relativedelta.relativedelta(years=1)
                dateRange['start']="%s" %temp_date.date()
                num_days=pdt.calendar.monthrange(temp_date.year, temp_date.month)[1]
                dateRange['end']=("%s" %(temp_date+datetime.timedelta(num_days-1))).split()[0]
                dateRange['string']=match.group()
                return dateRange
                    #for january, last october
                    #dreturn "Please provide valid range of dates."
          
            
        if not ("quarter" in message):
            t1=self.last_phrase_handle(message)
            if t1 is None:
                if len(dateOutput) == 1:
                    
                    dateRange['start'] = self.cal.parseDT(dateOutput[0].strip(),self.now)[0]
                    
                    if (dateRange['start']-self.now).days>0:
                        dateRange['start']=self.reduce_year(dateRange['start'])
                    validity=re.findall(r'\d+',dateOutput[0])    #checking validity of dates
                    validity=[int(i) for i in validity]  
                    
                    if dateRange['start'].day not in validity:     
                        return None
                    dateRange['start']=("%s" %dateRange['start']).split()[0]
                    dateRange['end']=dateRange['start']
                    dateRange['string']=dateOutput[0]
                    return dateRange
            else:
                return t1
        else: #for quarter
            message = self.text2int(message)  
            dateRange = {}
            
            for matchedtext in re.findall(r'(this|current|last|previous|next|prior)(\s\d+\s)(quarter|quarters)|(this|current|last|previous|next|prior)(\s)(quarter|quarters)', message):
                matchedtext = ''.join(matchedtext).strip()
                matchedInt = re.findall(r'\d+', matchedtext)
                #this_date = datetime.datetime.today()
                this_date=self.now
                year = this_date.year
                quarters = self.quartersRule(year)
                dateRange['string']=matchedtext
                if("last" in matchedtext or "previous" in matchedtext or "prior" in matchedtext):
                    no_of_days=0
                    if len(matchedInt) > 0:
                        no_of_days=int(matchedInt[0])*90
                    else:
                        no_of_days=90
                    
                    day = (quarters.before(this_date)-relativedelta.relativedelta(days=no_of_days))
                    year = day.year
                    quartersDay = self.quartersRule(year)
                    start_day = quartersDay.before(day)
                    end_day = quarters.before(this_date)-relativedelta.relativedelta(days=1)
                    dateRange['start'] ="%s" %start_day.date()
                    dateRange['end'] = "%s" %end_day.date()
                        
                    
                        
                elif("next" in matchedtext):
                    if len(matchedInt) > 0:
                        no_of_days=int(matchedInt[0])*90
                    else:
                        no_of_days=90
                                                                     
                    day = (quarters.after(this_date)+relativedelta.relativedelta(days=no_of_days))
                    year = day.year
                    quartersDay = self.quartersRule(year)
                    start_day = quarters.after(this_date)
                    end_day = quartersDay.after(day)-relativedelta.relativedelta(days=1)
                    dateRange['start'] = "%s" %start_day.date()
                    dateRange['end'] = "%s" %end_day.date()
                   
                
                elif("this" in matchedtext or "current" in matchedtext):
                    no_of_days = 0
                    day = (quarters.after(this_date) + relativedelta.relativedelta(days=no_of_days))
                    year = day.year
                    quartersDay = self.quartersRule(year)
                    end_day = day-relativedelta.relativedelta(days=1)
                    start_day = quarters.before(this_date)
                    dateRange['start'] = "%s" %start_day.date()
                    dateRange['end'] = "%s" %end_day.date()
                
                return dateRange
            
dt = DateRangeExtractor()
#print(dt.rangeExtractor("I want to know the sales data of this quarter"))
#aa=dt.rangeExtractor("sales data  for last 5 quarters")
date_1=dt.rangeExtractor(" find product with sales between 10 and 20")
'''
x=date_1['start']
z=x.split('-')
date_1['start']=z[2]+'/'+z[1]+'/'+z[0]

x=date_1['end']
z=x.split('-')
date_1['end']=z[2]+'/'+z[1]+'/'+z[0]
'''

print(date_1)

       
