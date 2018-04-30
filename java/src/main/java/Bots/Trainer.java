package Bots;

import org.json.JSONObject;
import robocode.*;

public class Trainer extends AdvancedRobot {

    Connection conn = new Connection();
    BotProxy proxy = new BotProxy(this);
    Observation obs;

    public void run() {

        conn.open("localhost", 8888);
        int frame = 1;

        while (true) {
            int action = proxy.randomAction();
            obs = new Observation(getRoundNum() + 1, getNumRounds(), frame++, proxy.actionToString(action), getX(), getY(), getHeading());
            proxy.execAction(action);
            conn.send(obs.toJson().toString());
        }
    }

    public void onScannedRobot(ScannedRobotEvent e) {

        if (obs == null)
            return;

        obs.scanned = true;
        obs.scanned_enemy_distance = e.getDistance();

        double lastEnemyBearing = e.getBearing() % 360;

        // Calculate the angle to the scanned robot
        double angle = Math.toRadians((getHeading() + lastEnemyBearing));
        double enemyX = getX() + Math.sin(angle) * obs.scanned_enemy_distance;
        double enemyY = getY() + Math.cos(angle) * obs.scanned_enemy_distance;

        //absolute angle to enemy
        obs.scanned_enemy_bearing = Util.absBearing(
                (float)getX(),
                (float)getY(),
                (float)enemyX,
                (float)enemyY);

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

}
