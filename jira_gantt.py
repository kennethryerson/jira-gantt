import datetime
import gantt
from jira import JIRA

class JiraVersionChart(object):
    """A chart of Jira project versions"""
    def __init__(self, project):
        self.project = project

    def generate_chart(self):
        """
        Creates a version chart SVG.
        """
        p = gantt.Project(name=self.project.name)
        for version in self.project.versions:
            if hasattr(version, 'startDate') and hasattr(version, 'releaseDate'):
                start_date = (int(x) for x in version.startDate.split('-'))
                end_date = (int(x) for x in version.releaseDate.split('-'))
                task = gantt.Task(name=version.name,
                                  start=datetime.date(*start_date),
                                  stop=datetime.date(*end_date))
                p.add_task(task)
        today = datetime.date.today()
        p.make_svg_for_tasks(filename='{0}_dy.svg'.format(self.project.key),
                             today=today,
                             scale=gantt.DRAW_WITH_DAILY_SCALE)
        p.make_svg_for_tasks(filename='{0}_wk.svg'.format(self.project.key),
                             today=today,
                             scale=gantt.DRAW_WITH_WEEKLY_SCALE)

class JiraConnection(object):
    """Manages a connection to a Jira database"""
    def __init__(self):
        self.jira = None
        self.project = None

    def connect(self, url, user, passwd):
        """
        Connect to a Jira server

        Arguments:
        url    -- URL of the Jira server
        user   -- username
        passwd -- password
        """
        options = {'server': url}
        self.jira = JIRA(options, basic_auth=(user, passwd))

    def get_project_list(self):
        """
        Returns a list of available projects.
        Projects are tuples with the format (key, name).
        """
        plist = []
        for project in self.jira.projects():
            plist.append((project.key, project.name))
        return plist

    def set_project(self, key):
        """
        Sets the active project.

        Arguments:
        key -- project key
        """
        self.project = self.jira.project(key)
