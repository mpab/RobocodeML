package Bots;

import com.sun.javafx.geom.Point2D;

import java.util.Random;

public class Util {
	public static double qPos(double pos) {
		return pos / 100;
	}
	
	public static int qDist(double dist) {
		return (int)Math.floor(dist / 250);
	}
	
	public static double absBearing(float x1, float y1, float x2, float y2) {
		double xd = x2 - x1;
		double yd = y2 - y1;
        double hyp = Math.hypot(xd, yd);
		double arcSin = Math.toDegrees(Math.asin(xd / hyp));
		double bearing = 0;

		// determine quadrant
		if (xd > 0 && yd > 0) { // both pos: lower-Left
			return arcSin;
		} else if (xd < 0 && yd > 0) { // x neg, y pos: lower-right
			return 360 + arcSin;
		} else if (xd > 0 && yd < 0) { // x pos, y neg: upper-left
			return 180 - arcSin;
		} else if (xd < 0 && yd < 0) { // both neg: upper-right
			return 180 - arcSin;
		}

		return bearing;
	}
	

}
