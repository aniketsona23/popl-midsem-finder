(defclass rectangle ()
	(
		(height :initform 0.0 :initarg :height)
		(width :initform 0.0 :initarg :width)
	)
)

(defclass color-mixin ()
	(
		(cyan :initform 0 :initarg :cyan)
		(magenta :initform 0 :initarg :magenta)
		(yellow :initform 0 :initarg :yellow)
	)
)

(defclass color-rectangle (color-mixin rectangle)
	(
		(clearp :initform (y-or-n-p "But is it transparent?")
			:initarg :clearp :accessor clearp)
	)
)

(defgeneric paint (x))

(defmethod paint ((x rectangle)) ;Method #1
	(vertical-stroke
		(slot-value x 'height)
		(slot-value x 'width)
	)
)

(defmethod paint :before ((x color-mixin)) ;Method #2
	(set-brush-color
		(slot-value x 'cyan)
		(slot-value x 'magenta)
		(slot-value x 'yellow)
	)
)

(defmethod paint ((x color-rectangle)) ;Method #3
	(unless (clearp x) (call-next-method))
)

(setq door
	(make-instance 'color-rectangle
		:width 38 :height 84 :cyan 60
		:yellow 55 :clearp nil
	)
)

