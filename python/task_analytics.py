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
        array = [[project, task.id, task.description, task.done, task.deadline, task] for project, tasks in tasks_dict.items() for task in tasks]
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
            completed_tasks=('done',np.sum),
            pending_tasks=('done', lambda x: x.count() - x.sum()),
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
        return df.loc[df['description'].str.lower().str.contains(keyword.lower())]
        
    def find_overdue_tasks(self, df: pd.DataFrame, current_date: str) -> pd.DataFrame:
        """Find all incomplete tasks past their deadline.
        """
        df_overdue = df.loc[df['deadline'] < datetime.strptime(current_date, '%d-%m-%Y')]
        df_overdue['deadline'] = pd.to_datetime(df_overdue['deadline'])
        return df_overdue

if __name__ == "__main__":
    analytics = TaskAnalytics()
    # input_dict = {'Food': [Task(1, "Eat donuts", False), Task(3, "Dinner", True)], 'Chores': [Task(2, 'Dishes', True), Task(4, "Clean floor", True)], 'Fun': [Task(5, 'Paint minis', False)]}
    # input_dict['Food'][1].deadline = '01-01-2027'
    # df = analytics.import_from_dict(input_dict)
    # print(df)
    # print(df.dtypes)
    # output_dict = analytics.export_to_dict(df)
    # print(output_dict)
    # analytics.export_to_csv(df, 'test.csv')
    # df2=analytics.import_from_csv('test.csv')
    # print(df2)
    # print(df2.dtypes)
    # summary = analytics.get_project_summary(df)
    # print(summary)
    # print(summary.dtypes)
    # print(analytics.get_top_projects_by_completion(df, 2))
    # print(analytics.find_tasks_by_keyword(df, 'clean'))
    # print(analytics.find_overdue_tasks(df, '06-06-2027'))
    task1 = Task(1, 'Eat donuts', False)
    task2 = Task(2, 'Dishes', True)
    task3 = Task(3, 'Dinner', True)
    task4 = Task(4, 'Clean floor', True)
    task5 = Task(5, 'Paint minis', False)
    df = pd.DataFrame([['Food', 1, 'Eat donuts', False, datetime(1999, 9, 3), task1],
                        ['Food', 3, 'Dinner', True, datetime(2027, 1, 1), task3],
                        ['Chores', 2, 'Dishes', True, datetime(3000,5,13), task2],
                        ['Chores', 4, 'Clean floor', True, pd.NaT, task4],
                        ['Fun', 5, 'Paint minis', False, pd.NaT, task5]
                        ], columns=['project_name','task_id','description','done','deadline','task'])
    df_overdue = analytics.find_overdue_tasks(df, '22-01-2050')
    print(df_overdue)
    test_df = pd.DataFrame([['Food', 1, 'Eat donuts', False, datetime(1999, 9, 3), task1],
                        ['Food', 3, 'Dinner', True, datetime(2027, 1, 1)], task3], 
                        columns=['project_name','task_id','description','done','deadline','task'], 
                        index=[0,1])
    # print(test_df)
    # print(df_overdue.equals(test_df))