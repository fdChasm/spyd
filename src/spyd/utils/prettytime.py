import datetime

def getComponent(value, identifier):
	if value <= 0:
		return ""
	returnValue = str(value) + " " + str(identifier)
	if value == 1:
		return returnValue
	else:
		return returnValue + "s"

def createDurationString(seconds):
	timeObject = datetime.timedelta(seconds=seconds)

	years = int(timeObject.days / 365)
	days = int(timeObject.days % 365)
	hours = int(timeObject.seconds / 3600)
	minutes = int(int(timeObject.seconds % 3600) / 60)
	seconds = int(int(timeObject.seconds % 3600) % 60)

	timeList = []

	component = getComponent(years, "year")
	if component != "":
		timeList.append(component)

	component = getComponent(days, "day")
	if component != "":
		timeList.append(component)

	component = getComponent(hours, "hour")
	if component != "":
		timeList.append(component)

	component = getComponent(minutes, "minute")
	if component != "":
		timeList.append(component)

	component = getComponent(seconds, "second")
	if component != "":
		timeList.append(component)

	if len(timeList) == 0:
		return "0 seconds"

	if len(timeList) == 1:
		return timeList[0]

	if len(timeList) > 2:
		timeList = [', '.join(timeList[:-1]), timeList[-1]]

	return ', and '.join(timeList)

def getShortComponent(value, identifier):
	if value <= 0: return ""
	return "{}{}".format(value, identifier)

def shortDurationString(seconds):
	timeObject = datetime.timedelta(seconds=seconds)

	years = int(timeObject.days / 365)
	days = int(timeObject.days % 365)
	hours = int(timeObject.seconds / 3600)
	minutes = int(int(timeObject.seconds % 3600) / 60)
	seconds = int(int(timeObject.seconds % 3600) % 60)

	timeList = []

	component = getShortComponent(years, "y")
	if component != "":
		timeList.append(component)

	component = getShortComponent(days, "d")
	if component != "":
		timeList.append(component)

	component = getShortComponent(hours, "h")
	if component != "":
		timeList.append(component)

	component = getShortComponent(minutes, "m")
	if component != "":
		timeList.append(component)

	component = getShortComponent(seconds, "s")
	if component != "":
		timeList.append(component)

	if len(timeList) == 0:
		return "0s"

	return ' '.join(timeList)
