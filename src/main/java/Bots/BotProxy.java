package Bots;

import robocode.AdvancedRobot;
import robocode.Rules;
import robocode.ScannedRobotEvent;

import java.util.Random;

import static robocode.util.Utils.normalRelativeAngleDegrees;

public class BotProxy {
    public AdvancedRobot bot;
	public double lastEnemyBearing = 0;

	public int action;

	public double enemyDistance;
    public double qEnemyDistance;

    public double enemyBearing;
	public double qEnemyBearing;
	
	public double enemyVelocity;

	public double turretTurn;
	
	public static final int NUM_ACTIONS = 5;

    Connection connection;
    int msgFrame = 0;

    public BotProxy(AdvancedRobot bot) {
        this.bot = bot;
    }

    public BotProxy(AdvancedRobot bot, Connection connection ) {
        this.bot = bot;
        this.connection = connection;
    }

    public int execRandomAction() {
        action = randomAction();
        execAction(action);
        return action;
    }

    private void cSend(String k, String v) {

        if (connection == null)
            return;

        if (!connection.isOpen()) {
            return;
        }

        connection.send(msgFrame, k, v);
    }

    private void cOpen(int round, int numRounds) {

        if (connection == null)
            return;

        if (connection.isOpen()) {
            return;
        }

        System.out.println("opening connection");
        connection.open(round, numRounds);
    }

    private void cClose() {

        if (connection == null)
            return;

        if (!connection.isOpen()) {
            return;
        }

        System.out.println("closing connection");
        connection.close();
        connection = null;
    }

	public void learn() {

        System.out.println("learn()");

        action = execRandomAction();

        if (!connection.isOpen()) {
            return;
        }

        ++msgFrame; // update frame counter for message

        cSend("action", actionToString());
        cSend("x", String.format("%f", bot.getX()));
        cSend("y", String.format("%f", bot.getY()));
        cSend("distance", String.format("%f", enemyDistance));
        cSend("bearing", String.format("%f", enemyBearing));
    }

    public int randomAction() {
		java.util.Random rand = new Random();
		// +1 makes range inclusive, 1 -> NUM_ACTIONS
		return rand.nextInt(NUM_ACTIONS) + 1;
	}

	public void fireAtEnemy() {
	    //if (Math.abs(bot.getGunTurnRemaining()) >= 0.35) {
	    //    return;
        //}

		if (bot.getGunHeat() > 0)
			return;

		double power = Rules.MAX_BULLET_POWER - qEnemyDistance;

		if (power < Rules.MIN_BULLET_POWER)
			power = Rules.MIN_BULLET_POWER;

        if (power > Rules.MAX_BULLET_POWER)
            power = Rules.MAX_BULLET_POWER;

		bot.fire(power);
	}

	public void onScannedRobot(ScannedRobotEvent e) {

		enemyVelocity = e.getVelocity();

		turretTurn = normalRelativeAngleDegrees(e.getBearing() + bot.getHeading() - bot.getRadarHeading());

        lastEnemyBearing = e.getBearing() % 360;

		// Calculate the angle to the scanned robot
		double angle = Math.toRadians((bot.getHeading() + lastEnemyBearing));
		double enemyX = bot.getX() + Math.sin(angle) * e.getDistance();
		double enemyY = bot.getY() + Math.cos(angle) * e.getDistance();

		//absolute angle to enemy
		enemyBearing = Util.absBearing(
				(float)bot.getX(),
				(float)bot.getY(),
				(float)enemyX,
				(float)enemyY);
        qEnemyBearing = Util.qDist(enemyBearing);

        enemyDistance = e.getDistance(); //distance to enemy feature
        qEnemyDistance = Util.qDist(enemyDistance);

        // now we have a full set of features, start transmission
        cOpen(bot.getRoundNum(), bot.getNumRounds());

		fireAtEnemy();
	}

	public String actionToString() {
        switch (action) {

            case 1:	// stop
                return "STOP";

            case 2:	// forwards
                return "FORWARD";

            case 3:	// backwards
                return "BACKWARD";

            case 4:	// cw
                return "CW";

            case 5:	// ccw
                return "CCW";

            default: // exception
                break;
        }
        return "ERROR";
    }

	public void execAction(int action) {

		switch (action) {

			case 1:	// stop
				bot.setAhead(0);
				break;

			case 2:	// forwards
				bot.setAhead(150);
				break;

			case 3:	// backwards
				bot.setAhead(-150);
				break;

			case 4:	// cw
				bot.setTurnRight(enemyBearing + 90);
				bot.setAhead(150);
				break;

			case 5:	// ccw
				bot.setTurnLeft(enemyBearing + 90);
				bot.setAhead(150);
				break;


			default: // exception
				bot.out.format("execAction - unhandled state %d\n", action);
		}

        bot.turnGunRight(360);
	}

    // robot collision
    public void onHitRobot() {
        cSend("event", "HitRobotEvent");
    }

    // we have shot an enemy
    public void onBulletHit() {

        cSend("event","BulletHitEvent");
    }

    // an enemy has shot us
    public void onHitByBullet() {

        cSend("event","HitByBulletEvent");
    }

    public void onHitWall() {

        cSend("event","HitWallEvent");
    }

    public void onBulletMissed() {

        cSend("event","BulletMissedEvent");
    }

    public void onBulletHitBullet() {

        cSend("event","BulletHitBulletEvent");
    }

    public void onWin() {
        cSend("event","WinEvent");
        cClose();
    }

    public void onBattleEnded() {
        cSend("event","BattleEndedEvent");
        cClose();
    }

    public void onRoundEnded() {
        cSend("event","RoundEndedEvent");
        cClose();
    }

}
