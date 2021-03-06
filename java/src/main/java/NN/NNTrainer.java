package NN;

import Common.BotProxy;
import Common.Connection;
import Common.Observation;
import robocode.*;

public class NNTrainer extends AdvancedRobot {

    public double lastEnemyBearing;
    public double lastEnemyDistance;
    public double lastEnemyX;
    public double lastEnemyY;

    public Connection conn = new Connection();
    public BotProxy proxy = new BotProxy(this);
    public Observation obs;

    public void run() {

        conn.open("localhost", 8888);
        int frame = 0;

        while (true) {
            int action = proxy.randomAction();
            obs = new Observation(getRoundNum() + 1, getNumRounds(), frame++, action);
            proxy.execAction(action);
            conn.send(obs.toJson().toString());
        }
    }

    public void onScannedRobot(ScannedRobotEvent e) {

        if (obs == null)
            return;

        // capture these features when scanned, otherwise they would be invalid
        obs.x = getX();
        obs.y = getY();
        obs.heading = getHeading();

        obs.scanned = true;
        lastEnemyDistance = e.getDistance();
        obs.scanned_enemy_distance = lastEnemyDistance;

        lastEnemyBearing = e.getBearing() % 360;

        // Calculate the angle to the scanned robot
        double angle = Math.toRadians((getHeading() + lastEnemyBearing));
        lastEnemyX = getX() + Math.sin(angle) * lastEnemyDistance;
        obs.scanned_enemy_x = lastEnemyX;
        lastEnemyY = getY() + Math.cos(angle) * lastEnemyDistance;
        obs.scanned_enemy_y = lastEnemyY;

        //absolute angle to enemy
        lastEnemyBearing = absBearing(
                (float)getX(),
                (float)getY(),
                (float)obs.scanned_enemy_x,
                (float)obs.scanned_enemy_y);
        obs.scanned_enemy_bearing = lastEnemyBearing;

        proxy.fireAtEnemy(obs.scanned_enemy_distance);
    }

    // robot collision
    public void onHitRobot(HitRobotEvent event) {
        if (obs == null)
            return;
        ++obs.enemy_collisions;
    }

    // we have shot an enemy
    public void onBulletHit(BulletHitEvent event) {
        if (obs == null)
            return;
        ++obs.shell_hits; }

    // an enemy has shot us
    public void onHitByBullet(HitByBulletEvent event) {
        if (obs == null)
            return;
        ++obs.shell_wounds;
    }

    public void onHitWall(HitWallEvent event) {
        if (obs == null)
            return;
        ++obs.wall_collisions;
    }

    public void onBulletMissed(BulletMissedEvent event) {
        if (obs == null)
            return;
        ++obs.shell_misses;
    }

    public void onBulletHitBullet(BulletHitBulletEvent event) {
        if (obs == null)
            return;
        ++obs.shell_intercepts;
    }

    public void onWin(WinEvent event) {
        conn.close();
    }

    public void onBattleEnded(BattleEndedEvent event) {
        conn.close();
    }

    public void onRoundEnded(RoundEndedEvent event) {
        conn.close();
    }

    private double absBearing(float x1, float y1, float x2, float y2) {
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
