PROPERTY_CHOICES = (
    ("coliving", "Coliving"),
    ("holidayhomes", "HolidayHomes"),
)
OCCUPANCY_TYPE = (
    ("1", "Single"),
    ("2", "Double"),
    ("3", "Triple"),
    ("4", "Quadruple"),
    ("5", "Quintuple"),
)
GENDER_CHOICES = (
    ("male", "Male"),
    ("female", "Female"),
    ("others", "Others"),
)

ROOM_CHOICE = (
    ("1", "Single"),
    ("2", "Double"),
    ("3", "Triple")
)

OCCUPATION = (("student", "Student"), ("professional", "Professional"))

STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]



CHOICE=[('unpaid', 'Unpaid'), ('paid', 'Paid')]