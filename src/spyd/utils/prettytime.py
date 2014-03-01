import datetime
from spyd.utils.listjoin import listjoin

def getComponent(value, identifier):
    if value <= 0:
        return ()

    returnValue = "{} {}".format(value, identifier)

    if value == 1:
        return (returnValue,)
    else:
        return (returnValue + "s",)

def createDurationString(seconds):
    timeObject = datetime.timedelta(seconds=seconds)

    years = int(timeObject.days / 365)
    days = int(timeObject.days % 365)
    hours = int(timeObject.seconds / 3600)
    minutes = int(int(timeObject.seconds % 3600) / 60)
    seconds = int(int(timeObject.seconds % 3600) % 60)

    timeList = []

    timeList.extend(getComponent(years, "year"))
    timeList.extend(getComponent(days, "day"))
    timeList.extend(getComponent(hours, "hour"))
    timeList.extend(getComponent(minutes, "minute"))
    timeList.extend(getComponent(seconds, "second"))

    if len(timeList) == 0:
        return "0 seconds"

    return listjoin(timeList)

def getShortComponent(value, identifier):
    if value <= 0: return ()
    return ("{}{}".format(value, identifier),)

def shortDurationString(seconds):
    timeObject = datetime.timedelta(seconds=seconds)

    years = int(timeObject.days / 365)
    days = int(timeObject.days % 365)
    hours = int(timeObject.seconds / 3600)
    minutes = int(int(timeObject.seconds % 3600) / 60)
    seconds = int(int(timeObject.seconds % 3600) % 60)

    timeList = []

    timeList.extend(getShortComponent(years, "y"))
    timeList.extend(getShortComponent(days, "d"))
    timeList.extend(getShortComponent(hours, "h"))
    timeList.extend(getShortComponent(minutes, "m"))
    timeList.extend(getShortComponent(seconds, "s"))

    if len(timeList) == 0:
        return "0s"

    return ' '.join(timeList)
