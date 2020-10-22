import { DateTime, Interval } from "luxon";

const HOUR_ONLY_FORMAT = {
  hour: "numeric",
  minute: "2-digit",
};

const SAME_YEAR_FORMAT = {
  weekday: "long",
  month: "long",
  day: "numeric",
  hour: "numeric",
  minute: "2-digit",
};

const OTHER_YEAR_FORMAT = {
  year: "numeric",
  month: "long",
  day: "numeric",
  hour: "numeric",
  minute: "2-digit",
};

export function dateFromISOString(s) {
  return DateTime.fromISO(s).setLocale("fr");
}

export function displayHumanDate(datetime, relativeTo) {
  if (relativeTo === undefined) {
    relativeTo = DateTime.local();
  }
  const interval =
    relativeTo < datetime
      ? Interval.fromDateTimes(relativeTo, datetime)
      : Interval.fromDateTimes(datetime, relativeTo);

  const qualifier = relativeTo < datetime ? "prochain" : "dernier";

  const calendarDays = interval.count("days");

  if (calendarDays <= 3) {
    const dayPart = datetime.toRelativeCalendar({ base: relativeTo });
    return `${dayPart} à ${datetime.toLocaleString(HOUR_ONLY_FORMAT)}`;
  } else if (calendarDays <= 8) {
    const dayPart = datetime.weekdayLong;
    return `${dayPart} ${qualifier} à ${datetime.toLocaleString(
      HOUR_ONLY_FORMAT
    )}`;
  } else if (interval.count("months") <= 4) {
    return datetime.toLocaleString(SAME_YEAR_FORMAT);
  } else {
    return datetime.toLocaleString(OTHER_YEAR_FORMAT);
  }
}

export function displayInterval(interval, relativeTo) {
  if (relativeTo === undefined) {
    relativeTo = DateTime.local().setLocale("fr");
  }

  const fromNowInterval =
    relativeTo < interval.start
      ? Interval.fromDateTimes(relativeTo, interval.start)
      : Interval.fromDateTimes(interval.start, relativeTo);

  const showYear = fromNowInterval.count("months") > 4;
  const scheduleCalendarDays = interval.count("days");

  const dayPartFormat = {
    year: showYear ? "numeric" : undefined,
    month: "long",
    day: "numeric",
  };

  if (scheduleCalendarDays === 1) {
    const dayPart = interval.start.toLocaleString(dayPartFormat);
    const hourPart = `de ${interval.start.toLocaleString(
      HOUR_ONLY_FORMAT
    )} à ${interval.end.toLocaleString(HOUR_ONLY_FORMAT)}`;
    return `le ${dayPart}, ${hourPart}`;
  }

  const start = interval.start.toLocaleString({
    ...dayPartFormat,
    ...HOUR_ONLY_FORMAT,
  });
  const end = interval.end.toLocaleString({
    ...dayPartFormat,
    ...HOUR_ONLY_FORMAT,
    year: undefined,
  });
  return `du ${start} au ${end}`;
}
