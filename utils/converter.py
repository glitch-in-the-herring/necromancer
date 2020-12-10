# Converts a timedelta object into seconds
def delta_to_secs(delta):
	return delta.days * 86400 + delta.seconds


# Converts a number of seconds into a tuple consisting of hours, minutes, and seconds
def secs_to_hms(seconds):
	hours, remainder = divmod(seconds, 3600)
	minutes, seconds = divmod(remainder, 60)
	return hours, minutes, seconds
	