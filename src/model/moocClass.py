from string import Template

class moocClass(object):
    def __init__(self, id, platform, institution, title, url, class_type, description, rating, rating_max, num_reviews, difficulty, duration, skills, prereqs, cost_type):
        self.id = id
        self.platform = platform
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
        self.cost_type = cost_type
    
    def toFileString(self):
        line = Template('$id,$platform,$institution,$title,$url,$class_type,$description,$rating,$rating_max,$num_reviews,$difficulty,$duration,$skills,$prereqs,$cost_type \n')
        self.platform.replace(",", "")
        self.institution.replace(",", "")
        self.title.replace(",", "")
        self.url.replace(",", "")
        self.class_type.replace(",", "")
        self.description.replace(",", "")
        self.num_reviews.replace(",", "")
        self.duration.replace(",", "")
        self.skills.replace(",", "")
        self.prereqs.replace(",", "")
        return(line.substitute(id=self.id,platform=self.platform,institution=self.institution,title=self.title,url=self.url,class_type=self.class_type,description=self.description,rating=self.rating,rating_max=self.rating_max,num_reviews=self.num_reviews,difficulty=self.difficulty,duration=self.duration,skills=self.skills,prereqs=self.prereqs,cost_type=self.cost_type))
        
    
    def toOutputString(self):
        if(self.rating == "None"):
            line = Template('Title: $title,\n\tPlatform: $platform,\n\tInstitution: $institution,\n\tURL: $url,\n\tType: $class_type,\n\tDescription: "$description",\n\tRating: $rating,\n\tDifficulty: $difficulty,\n\tDuration: $duration,\n\tSkills: $skills,\n\tPrerequisites: $prereqs,\n\tCost Type: $cost_type\n\n')
        else:
            line = Template('Title: $title,\n\tPlatform: $platform,\n\tInstitution: $institution,\n\tURL: $url,\n\tType: $class_type,\n\tDescription: "$description",\n\tRating: $rating out of $rating_max ($num_reviews reviews),\n\tDifficulty: $difficulty,\n\tDuration: $duration,\n\tSkills: $skills,\n\tPrerequisites: $prereqs,\n\tCost Type: $cost_type\n\n')
        return(line.substitute(platform=self.platform,institution=self.institution,title=self.title,url=self.url,class_type=self.class_type,description=self.description,rating=self.rating,rating_max=self.rating_max,num_reviews=self.num_reviews,difficulty=self.difficulty,duration=self.duration,skills=self.skills,prereqs=self.prereqs,cost_type=self.cost_type))