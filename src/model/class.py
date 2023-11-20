from string import Template

class Class:
    def __init__(self, id, institution, title, url, class_type, description, rating, rating_max, num_reviews, difficulty, duration, skills, prereqs, free):
        self.id = id
        self.institution = institution
        self.title = title
        self.url = url
        self.class_type = class_type
        self.description = description
        self.rating = rating
        self.rating_max = rating_max
        self.num_reviews = num_reviews
        self.difficulty = difficulty
        self.duration = duration
        self.skills = skills
        self.prereqs = prereqs
        self.free = free
    
    def toFileString(self):
        line = Template('$id,$institution,$title,$url,$class_type,$description,$rating,$rating_max,$num_reviews,$difficulty,$duration,$skills,$prereqs,$free')
        return(line.substitute(id=self.id,institution=self.institution,title=self.title,url=self.url,class_type=self.class_type,description=self.description,rating=self.rating,rating_max=self.rating_max,num_reviews=self.num_reviews,difficulty=self.difficulty,duration=self.duration,skills=self.skills,prereqs=self.prereqs,free=self.free))
        
    
    def toOutputString(self):
        line = Template('Title: $title,\n Institution: $institution,\n URL: $url,\n Type: $class_type,\n Description: $description,\n Rating: $rating out of $rating_max ($num_reviews reviews),\n Difficulty$difficulty,\n Duration: $duration,\n Skills: $skills,\n Prerequisites: $prereqs,\n Free: $free\n\n')
        return(line.substitute(institution=self.institution,title=self.title,url=self.url,class_type=self.class_type,description=self.description,rating=self.rating,rating_max=self.rating_max,num_reviews=self.num_reviews,difficulty=self.difficulty,duration=self.duration,skills=self.skills,prereqs=self.prereqs,free=self.free))