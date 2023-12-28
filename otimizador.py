import pandas as pd
import datetime as dt

global_freq = 'W-SAT'

def getSpecificDayofWeek (startDate='2023-07-15', endDate='2024-07-15', freq=global_freq):
    """
        W-SUN, W-MON, W-TUE, W-WED, W-THU, W-FRI, W-SAT
    """
    # Criação de todas as datas entre o startDate e endDate
    dates = pd.date_range(start=startDate, end=endDate, freq=freq)
    
    return dates

def validateWeekAlocation(row_company, week, phase_start, phase_end, vacation_weeks):
    """
        Função de validação da semana para verificar se é possível realizar a alocação do recurso ou não.
    """    
    
    if not pd.Timestamp(phase_start) <= week:
        print("Invalid: Semana não esta no range de datas desta fase.")
        return -1
    
    if not week <= pd.Timestamp(phase_end):
        print("Invalid: Semana não esta no range de datas desta fase.")
        return -2
    
    if row_company[week] >= 40:
        print("Invalid: Valor acima de 40.")
        return 0
    
    if week in vacation_weeks:
        print("Invalid: Semana de período de férias.")
        return 0
    
    return 1

def getWeekLowestHours(df_company, weeks=pd.DatetimeIndex([])):
    
    if weeks.empty:
        return None
    
    #  Calcular o desvio padrão de cada semana
    total_sum = df_company[weeks].sum()
    
    # Identificar qual semana tem o menor desvio padrão
    min_sum_week = total_sum.idxmin()
    
    return min_sum_week


def getVacationPeriod():
    
    df_phase = pd.read_csv('bases/fases_projetos.csv', sep=';')
    code='fase_ferias'
    
    filter_phases_vacation = df_phase[df_phase['code'] == 'fase_ferias']
    
    all_dates = []
    
    for index, row in filter_phases_vacation.iterrows():
        data_range = pd.date_range(start=row['start'], periods=2, freq='W-SAT')
        all_dates.extend(data_range)

    return all_dates

def filterCompanyPhases(rowCompany, df_phase):
    """
        Função para filtrar as phases de um empresa para realizar a alocação dos recursos.
    """
    #Definir se é empresa Grande ou Pequena
    values_filter = ['P'] if rowCompany['horas'] > 2000 else ['G']
    
    # Remover as fases de Férias
    values_filter.append('F')
    
    # Caso não tenha trimestral remover estas fase tambem
    if rowCompany['possui trimestral'] == 'No':
        values_filter.append('T')
    
    return df_phase[~df_phase['part'].isin([values_filter])]

def getValidWeekLowestHours(df_company, row_company, week_min, week_max, phase_start, phase_end, vacation_weeks):
        
    week_min_valid = validateWeekAlocation(row_company, week_min, phase_start, phase_end, vacation_weeks)
    while week_min_valid != 1 and week_min >= pd.Timestamp(phase_start):
        week_min -= dt.timedelta(weeks=1)
        week_min_valid = validateWeekAlocation(row_company, week_min, phase_start, phase_end, vacation_weeks)
    
    week_max_valid = validateWeekAlocation(row_company, week_max, phase_start, phase_end, vacation_weeks)
    
    while week_max_valid != 1 and week_max <= pd.Timestamp(phase_end):
        week_max += dt.timedelta(weeks=1)
        week_max_valid = validateWeekAlocation(row_company, week_max, phase_start, phase_end, vacation_weeks)
        
    weeks_compare = pd.DatetimeIndex([])
    
    if week_min_valid == 1:
        weeks_compare = weeks_compare.union([week_min])
        
    if week_max_valid == 1:
        weeks_compare = weeks_compare.union([week_max])
    
    return getWeekLowestHours(df_company, weeks_compare), week_min, week_max

def insertPhaseWeek(df_company, index_company, row_company, row_phase, vacation_weeks):
    """
        Função de validação da semana para verificar se é possível realizar a alocação do recurso ou não.

        - Obter a empresa
        - Obter a lista de fases
        - Filtrar as fases especificas para a empresa passada 
        - Para cada fase verificar a data de inicio e fim
        - 
    """
    
    phase_code = row_phase['code']
    phase_start = pd.Timestamp(row_phase['start'])
    phase_end = pd.Timestamp(row_phase['end'])

    phase_interval = (phase_end - phase_start).days // 7 

    if phase_code == 'fase_ferias':
        return    

    total_period = phase_interval if row_company[phase_code] > phase_interval else row_company[phase_code]
    
    # Obtem a primeira semana com o menor somatório de horas para alocar os recursos
    first_week = getWeekLowestHours(df_company, getSpecificDayofWeek(phase_start, phase_end).difference(vacation_weeks))  
    
    if phase_code == 'fase_final':
        first_week = pd.Timestamp(phase_end)
        if phase_interval > row_company[phase_code]:
            total_period = row_company[phase_code] if row_company[phase_code] > 4 else 5
            
        
    week_current = first_week
    week_max = first_week
    week_min = first_week
    
    for i in range(total_period):
        
        while (week_current != None):
            
            week_current, week_max, week_min = getValidWeekLowestHours(df_company, row_company, week_min, week_max
                                                                       , phase_start, phase_end, vacation_weeks)
    
            if week_current != None:
                row_company[week_current] += 40
                df_company.loc[index_company, week_current] += 40
                break
                

def replaceCurrentWeek(week_current, week_min, week_max):
    if week_current == week_min:
        week_min = week_min - dt.timedelta(weeks=1)
    
    if week_current == week_max:
        week_max = week_max + dt.timedelta(weeks=1)
    
    return week_min, week_max
    
                
def getOutputStructure(df_company, start_date, end_date):
    
    df_list_days = pd.DataFrame(getSpecificDayofWeek(start_date, end_date), columns=['data'])
    
    df_list_days = pd.DataFrame([], columns=df_list_days['data'])
    
    df_result = pd.concat([df_company, df_list_days], axis=1).fillna(0)
    
    return df_result

def arrangeAllResources(df_company, df_phases, start_date, end_date):
    
    vacation_weeks = getVacationPeriod()
    
    df_result = getOutputStructure(df_company, start_date, end_date)
    
    for index_result, row_result in df_result.iterrows():
    
        df_company_phase = filterCompanyPhases(row_result, df_phases)
        
        for index_phase, row_phase in df_company_phase.iterrows():
        
            insertPhaseWeek(df_result, index_result, row_result, row_phase, vacation_weeks)
    
    for col in df_result.columns:
        if isinstance(col, dt.datetime):
            df_result.rename(columns={col: col.strftime('%Y-%m-%d')}, inplace=True)
    
    df_result.to_excel('Resultado.xlsx', index=False)
