from __future__ import annotations

import datetime as dt
from datetime import date, datetime, time
from typing import List, Union

import pandas as pd
from dateutil.relativedelta import relativedelta, SA

import allocpro.config as cfg


TimestampOrDatetimeLike = Union[pd.Timestamp, datetime, date, time]


def get_specific_day_of_week(
    start_date: str = "2023-07-15",
    end_date: str = "2024-07-15",
    freq: str = "W-SAT",
):
    """
    Generate a list of dates for a specific day of the week within a given date range.

    This function creates a list of dates that fall on a specific day of the week
    (e.g., every Saturday) between the specified start and end dates.

    Parameters
    ----------
    start_date : str, default="2023-07-15"
        The start date of the range in "YYYY-MM-DD" format.
    end_date : str, default="2024-07-15"
        The end date of the range in "YYYY-MM-DD" format.
    freq : str, default="W-SAT"
        The frequency string representing the specific day of the week.
        This parameter also specifies which day of the week is considered as the
        first day of the week. It should be one of "W-SUN", "W-MON", "W-TUE",
        "W-WED", "W-THU", "W-FRI", "W-SAT".

    Returns
    -------
    pandas.DatetimeIndex
        A list of dates that fall on the specified day of the week within the given date range.

    Examples
    --------
    Create a list of dates between "2023-07-15" and "2023-08-15", where each
    date of the generated list is the week's Saturday:
    >>> get_specific_day_of_week("2023-07-15", "2023-07-23", "W-SAT")
    DatetimeIndex(['2023-07-15', '2023-07-22'], dtype='datetime64[ns]', freq='W-SAT')

    Function also supports mixed date formats:
    >>> get_specific_day_of_week("2023-07-15", "23/07/2023", "W-SAT")
    DatetimeIndex(['2023-07-15', '2023-07-22'], dtype='datetime64[ns]', freq='W-SAT')

    Even though the function allows you to define `start_date` and `end_date` dates
    using different date formats, this behavior should be avoided. Depending on the
    dates, specifying mixed formats can lead to unexpected behavior. For example,
    >>> get_specific_day_of_week("01/07/2023", "2023-07-23", "W-SAT")  # doctest: +ELLIPSIS
    DatetimeIndex(['2023-01-07', '2023-01-14', '2023-01-21',
    ...
    '2023-07-15', '2023-07-22'], dtype='datetime64[ns]', freq='W-SAT')
    """
    dates = pd.date_range(start=start_date, end=end_date, freq=freq)
    return dates


def validate_week_allocation(
    row_company: pd.Series | dict,
    week: TimestampOrDatetimeLike,
    phase_start: str | TimestampOrDatetimeLike,
    phase_end: str | TimestampOrDatetimeLike,
    vacation_weeks: List[TimestampOrDatetimeLike],
) -> int:
    """
    Validates if a resource can be allocated for a given week.

    This function checks if the specified week falls within the phase start
    and end dates, if the resource allocation for that week doesn't exceed 40 hours,
    and if the week is not a vacation week.

    Parameters
    ----------
    row_company : pandas.Series or dict
        A `pandas.Series` or dictionary representing the company's resource
        allocation per week.
    week : pandas.Timestamp or datetime-like
        The week to be validated for resource allocation.
    phase_start : str or datetime-like
        The start date of the phase.
    phase_end : str or datetime-like
        The end date of the phase.
    vacation_weeks : list of pandas.Timestamp or datetime-like
        A list of weeks that are considered vacation periods.

    Returns
    -------
    int
        An integer indicating the validation result:

            - -1 if the week is before the phase start date.
            - -2 if the week is after the phase end date.
            - 0 if the resource allocation exceeds 40 hours or if the week is a vacation week.
            - 1 if the week is valid for resource allocation.
    """
    if week < pd.Timestamp(phase_start):
        print("Invalid: Semana não esta no range de datas desta fase.")
        return -1

    if week > pd.Timestamp(phase_end):
        print("Invalid: Semana não esta no range de datas desta fase.")
        return -2

    if row_company[week] >= 40:
        print(f"Invalid: Valor igual ou acima de 40 ({row_company[week]}).")
        return 0

    if week in vacation_weeks:
        print("Invalid: Semana de período de férias.")
        return 0

    return 1


def get_week_lowest_hours(
    df_company: pd.DataFrame,
    weeks: pd.DatetimeIndex = pd.DatetimeIndex([]),
) -> pd.Timestamp | None:
    """
    Get the week with the lowest total hours from the specified weeks.

    This function calculates the total hours for each specified week and
    returns the week with the lowest total hours.

    Parameters
    ----------
    df_company : pandas.DataFrame
        A DataFrame representing the company's resource allocation.
    weeks : pandas.DatetimeIndex, default=pd.DatetimeIndex([])
        A list of weeks to be evaluated.

    Returns
    -------
    pandas.Timestamp or None
        The week with the lowest total hours. If `weeks` is empty, returns None.

    Notes
    -----
    If `weeks` is empty, the function will return None without performing any
    calculations.

    Examples
    --------
    >>> df = pd.DataFrame({
    ...     pd.Timestamp('2023-07-01'): [10, 20, 30],
    ...     pd.Timestamp('2023-07-08'): [15, 25, 5],
    ...     pd.Timestamp('2023-07-15'): [20, 5, 10]
    ... })
    >>> weeks = pd.DatetimeIndex(['2023-07-01', '2023-07-08', '2023-07-15'])
    >>> get_week_lowest_hours(df, weeks)
    Timestamp('2023-07-08')
    """
    if weeks.empty:
        return None

    # Calculates the standard deviation for each week
    total_sum = df_company[weeks].sum()

    # Identifies which week has the smallest standard deviation
    min_sum_week = total_sum.idxmin()

    return min_sum_week


def get_vacation_period() -> List[pd.Timestamp]:
    """
    Retrieve the vacation period dates from the project phases file.

    This function reads the project phases file and filters out the vacation
    phases. It then generates a list of dates that represent the vacation
    periods based on the filtered data.

    Returns
    -------
    list of pandas.Timestamp
        A list of dates that fall within the vacation periods.

    Examples
    --------
    >>> get_vacation_period()
    [Timestamp('2023-07-01 00:00:00', freq='W-SAT'),
    Timestamp('2023-07-08 00:00:00', freq='W-SAT'), ...]

    Notes
    -----
    The function assumes the project phases file is located at
    `cfg.FASES_PROJETO_FILEPATH` and is in CSV format with a semicolon
    separator. The CSV file must contain columns 'code', 'start', and
    'end' to properly filter and generate the vacation period dates.
    """
    df_phase = pd.read_csv(cfg.FASES_PROJETO_FILEPATH, sep=";")
    code = "fase_ferias"

    filter_phases_vacation = df_phase[df_phase["code"] == "fase_ferias"]

    all_dates = []

    for index, row in filter_phases_vacation.iterrows():
        data_range = pd.date_range(start=row["start"], periods=2, freq="W-SAT")
        all_dates.extend(data_range)

    return all_dates


def filter_company_phases(row_company, df_phase):
    """
    Filtra as fases de uma empresa para realizar a alocação dos recursos.
    """
    # Definir se é empresa Grande ou Pequena
    values_filter = ["P"] if row_company["horas"] > 2000 else ["G"]

    # Remover as fases de Férias
    values_filter.append("F")

    # Caso não tenha trimestral remover esta fase também
    if row_company["possui trimestral"] == "No":
        values_filter.append("T")

    return df_phase[~df_phase["part"].isin(values_filter)]


def get_valid_week_lowest_hours(
    df_company, row_company, week_min, week_max, phase_start, phase_end, vacation_weeks
):
    week_min_valid = validate_week_allocation(row_company, week_min, phase_start,
                                              phase_end, vacation_weeks)
    while week_min_valid != 1 and week_min >= pd.Timestamp(phase_start):
        week_min -= dt.timedelta(weeks=1)
        week_min_valid = validate_week_allocation(row_company, week_min, phase_start,
                                                  phase_end, vacation_weeks)

    week_max_valid = validate_week_allocation(row_company, week_max, phase_start,
                                              phase_end, vacation_weeks)

    while week_max_valid != 1 and week_max <= pd.Timestamp(phase_end):
        week_max += dt.timedelta(weeks=1)
        week_max_valid = validate_week_allocation(row_company, week_max, phase_start,
                                                  phase_end, vacation_weeks)

    weeks_compare = pd.DatetimeIndex([])

    if week_min_valid == 1:
        weeks_compare = weeks_compare.union([week_min])

    if week_max_valid == 1:
        weeks_compare = weeks_compare.union([week_max])

    return get_week_lowest_hours(df_company, weeks_compare), week_min, week_max


def insert_phase_week(
    df_company, index_company, row_company, row_phase, vacation_weeks
):
    """
    Verifica se é possível realizar a alocação do recurso ou não na semana.

    - Obtêm a empresa
    - Obtêm a lista de fases
    - Filtra as fases específicas para a empresa anterior
    - Para cada fase determina a data de início e fim
    """
    phase_code = row_phase["code"]
    phase_start = pd.Timestamp(row_phase["start"])
    phase_end = pd.Timestamp(row_phase["end"])
    phase_interval = (phase_end - phase_start).days // 7

    if phase_code == "fase_ferias":
        return

    total_period = (
        phase_interval
        if row_company[phase_code] > phase_interval
        else row_company[phase_code]
    )

    # Obtêm a primeira semana com o menor somatório de horas para alocar os recursos
    first_week = get_week_lowest_hours(
        df_company,
        get_specific_day_of_week(phase_start, phase_end).difference(vacation_weeks),
    )

    if phase_code == "fase_final":
        # first_week = pd.Timestamp(phase_end)
        if phase_interval > row_company[phase_code]:
            total_period = row_company[phase_code]
            if row_company[phase_code] <= 4:

                # Finding the last week of January, as small businesses should only
                # begin the "final phase" starting at the last week of January.
                phase_start = (
                    datetime(pd.to_datetime(row_phase["start"]).year, 1, 31)
                    + relativedelta(weekday=SA(-1))
                )

                # phase_start = pd.Timestamp(row_phase["start"]) + dt.timedelta(weeks=5)
                print(phase_start)

    week_current = first_week
    week_max = first_week
    week_min = first_week

    for i in range(total_period):
        while week_current is not None:
            week_current, week_max, week_min = get_valid_week_lowest_hours(df_company,
                                                                           row_company,
                                                                           week_min,
                                                                           week_max,
                                                                           phase_start,
                                                                           phase_end,
                                                                           vacation_weeks)

            if week_current is not None:
                row_company[week_current] += 40
                df_company.loc[index_company, week_current] += 40
                break


def get_output_structure(df_company, start_date, end_date):
    df_list_days = pd.DataFrame(
        get_specific_day_of_week(start_date, end_date), columns=["data"]
    )

    df_list_days = pd.DataFrame([], columns=df_list_days["data"])
    df_result = pd.concat([df_company, df_list_days], axis=1).fillna(0)

    return df_result


def arrange_all_resources(df_company, df_phases, start_date, end_date):
    vacation_weeks = get_vacation_period()

    df_result = get_output_structure(df_company, start_date, end_date)

    for index_result, row_result in df_result.iterrows():
        df_company_phase = filter_company_phases(row_result, df_phases)

        for index_phase, row_phase in df_company_phase.iterrows():
            insert_phase_week(df_result, index_result, row_result, row_phase,
                              vacation_weeks)

    for col in df_result.columns:
        if isinstance(col, dt.datetime):
            df_result.rename(columns={col: col.strftime("%Y-%m-%d")}, inplace=True)

    df_result.to_excel(cfg.RESULTADO_FILEPATH, index=False)
