import datetime
import gantt

class JiraVersionChart(object):
    def __init__(self, project):
        self.project = project

    def generate_chart(self):
        p = gantt.Project(name=self.project.name)
        for version in self.project.versions:
            task = gantt.Task(name=version.name,
                start=datetime.date(*version.startDate.split('-'),
                end=datetime.date(*version.releaseDate.split('-'))
            p.add_task(task)
        p.make_svg_for_tasks(filename='{0}.svg'.format(self.project.key),
                             today=datetime.datetime.now())

