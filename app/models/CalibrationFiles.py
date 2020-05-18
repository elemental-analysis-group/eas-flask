from app import db

class CalibrationFiles(db.Model):
    __tablename__ = 'calibration_files'

    id = db.Column(db.Integer, primary_key=True)
    csv_file = db.Column(db.Text)
    txt_file = db.Column(db.Text)
    standard_target = db.Column(db.Text)

    # calibration id
    calibration_id = db.Column(db.Integer, db.ForeignKey('calibrations.id'))
    calibration = db.relationship('Calibration',foreign_keys=calibration_id)

    def __init__(self, csv_file, txt_file, standard_target, calibration_id):
        self.csv_file = csv_file
        self.txt_file = txt_file
        self.standard_target = standard_target
        self.calibration_id = calibration_id

    def __repr__(self):
        return '<id %r>' % (self.id)



