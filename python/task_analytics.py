import pandas as pd
from typing import Dict, List
from task import Task
import numpy as np
from datetime import datetime

class TaskAnalytics:
    
    def import_from_dict(self, tasks_dict: Dict[str, List[Task]]) -> pd.DataFrame:
        """Import tasks from dictionary structure and convert to DataFrame.
        
        Note:
        - The 'done' column should be converted to boolean
        - The 'task_id' column should be converted to int
        - The 'deadline' column should be converted to datetime
        """
        array = [
            [project, task.id, task.description, task.done, task.deadline, task] for project, tasks in tasks_dict.items() for task in (tasks if len(tasks)>0 else [Task(None,'',None)])
        ]
        df = pd.DataFrame(array, columns=['project_name', 'task_id', 'description', 'done', 'deadline', 'task'])
        df['deadline'] = pd.to_datetime(df['deadline'], format='%d-%m-%Y')
        return df
    
    def export_to_dict(self, df: pd.DataFrame) -> Dict[str, List[Task]]:
        """Export DataFrame back to dictionary structure.
        """
        return df.groupby('project_name')['task'].apply(list).to_dict()

    
    def export_to_csv(self, df: pd.DataFrame, filepath: str) -> None:
        """Export tasks DataFrame to a CSV file.
        
        Note:
        - Use pandas to_csv() to save the DataFrame to a CSV file.
        """
        df.to_csv(filepath, columns=['project_name','task_id','description','done','deadline'], index=False, date_format='%d-%m-%Y')
    
    def import_from_csv(self, filepath: str) -> pd.DataFrame:
        """Import tasks from a CSV file into a DataFrame.
        
        Note:
        - Use pandas read_csv() to load the Dataframe from a CSV file.
        - The 'done' column should be converted to boolean
        - The 'task_id' column should be converted to int
        - The 'deadline' column should be converted to datetime
        """
        df = pd.read_csv(filepath, 
                         names=['project_name', 'task_id', 'description','done','deadline'], 
                         dtype={'project_name': str, 'task_id':np.dtype("int64"), 'description':str, 'done':bool,'deadline':str}, 
                         header=0
                         )
        df['deadline'] = pd.to_datetime(df['deadline'], format='%d-%m-%Y')
        return df
      
    def get_project_summary(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate a summary DataFrame for all projects.
        
        Create a DataFrame with one row per project containing:
        - project_name
        - total_tasks
        - completed_tasks
        - pending_tasks
        - completion_rate (percentage)
        """
        df_grouped = df.groupby(['project_name'], as_index=False).agg(
            total_tasks=('task_id','count'), 
            completed_tasks=('done',lambda x: int(x.sum(skipna=True))),
            pending_tasks=('done', lambda x: x.count() - x.sum(skipna=True)),
            completion_rate=('done', lambda x: 100*np.mean(x))
        )
        return df_grouped
    
    def get_top_projects_by_completion(self, df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
        """Get the top N projects with the highest completion rates.
        
        Create a DataFrame with one row per project containing:
        - project_name
        - completion_rate (percentage)
        """
        return df.groupby(['project_name'], as_index=False).agg(completion_rate=('done',lambda x: 100*np.mean(x))).sort_values(by=['completion_rate'], ascending=False).head(n)
    
    def find_tasks_by_keyword(self, df: pd.DataFrame, keyword: str) -> pd.DataFrame:
        """Find all tasks containing a specific keyword in their description.
        """
        return df.loc[df['description'].str.lower().str.contains(keyword.lower())][['project_name', 'task_id', 'description', 'done', 'deadline']]
        
    def find_overdue_tasks(self, df: pd.DataFrame, current_date: str) -> pd.DataFrame:
        """Find all incomplete tasks past their deadline.
        """
        df_overdue = df.loc[df['deadline'] < datetime.strptime(current_date, '%d-%m-%Y')]
        df_overdue['deadline'] = pd.to_datetime(df_overdue['deadline'])
        return df_overdue[['project_name', 'task_id', 'description', 'done', 'deadline']]