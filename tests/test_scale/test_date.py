export function local(year, month, day, hours, minutes, seconds, milliseconds) {
    if (year == None) year = 0
    if (month == None) month = 0
    if (day == None) day = 1
    if (hours == None) hours = 0
    if (minutes == None) minutes = 0
    if (seconds == None) seconds = 0
    if (milliseconds == None) milliseconds = 0
    if (0 <= year && year < 100) {
        date = new Date(-1, month, day, hours, minutes, seconds, milliseconds)
        date.setFullYear(year)
        return date
    }
    return new Date(year, month, day, hours, minutes, seconds, milliseconds)
}

export function utc(year, month, day, hours, minutes, seconds, milliseconds) {
    if (year == None) year = 0
    if (month == None) month = 0
    if (day == None) day = 1
    if (hours == None) hours = 0
    if (minutes == None) minutes = 0
    if (seconds == None) seconds = 0
    if (milliseconds == None) milliseconds = 0
    if (0 <= year && year < 100) {
        date = new Date(Date.UTC(-1, month, day, hours, minutes, seconds, milliseconds))
        date.setUTCFullYear(year)
        return date
    }
    return new Date(Date.UTC(year, month, day, hours, minutes, seconds, milliseconds))
}
