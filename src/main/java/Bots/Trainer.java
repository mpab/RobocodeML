package Bots;

import org.json.JSONObject;
import robocode.*;

public class Trainer extends AdvancedRobot {

    private BotProxy proxy = new BotProxy(this);
    Connection connection = new Connection();

    int frame = 0;

    // features
    int action;
    double distance;
    double bearing;
    // plus x, y

    // events
    int enemy_collisions;
    int enemy_hits;
    int wounds;
    int wall_collisions;
    int bullet_misses;
    int bullet_intercepts;

    public void run() {

        connection.open();

        while (true) {
            action = proxy.randomAction();
            proxy.execAction(action);
            netUpdate();
        }
    }

    private void resetEvents() {
        enemy_collisions = 0;
        enemy_hits = 0;
        wounds = 0;
        wall_collisions = 0;
        bullet_misses = 0;
        bullet_intercepts = 0;
    }

    public void onScannedRobot(ScannedRobotEvent e) {

        distance = e.getDistance();

        double lastEnemyBearing = e.getBearing() % 360;

        // Calculate the angle to the scanned robot
        double angle = Math.toRadians((getHeading() + lastEnemyBearing));
        double enemyX = getX() + Math.sin(angle) * distance;
        double enemyY = getY() + Math.cos(angle) * distance;

        //absolute angle to enemy
        bearing = Util.absBearing(
                (float)getX(),
                (float)getY(),
                (float)enemyX,
                (float)enemyY);

        proxy.fireAtEnemy(distance);
    }

    private JSONObject createTrainMsg() {
        JSONObject msg = new JSONObject();
        msg.put("frame", frame);
        msg.put("round", getRoundNum());
        msg.put("num_rounds", getNumRounds());
        return msg;
    }

    private void netUpdate() {
        ++frame; // update frame counter for message
        JSONObject msg = createTrainMsg();

        // actions
        msg.put("type", "action");
        msg.put("action", action);
        msg.put("x", getX());
        msg.put("y", getY());
        msg.put("distance", distance);
        msg.put("bearing", bearing);

        // events
        msg.put("enemy_collisions", enemy_collisions);
        msg.put("enemy_hits", enemy_hits);
        msg.put("wounds", wounds);
        msg.put("wall_collisions", wall_collisions);
        msg.put("bullet_misses", bullet_misses);
        msg.put("bullet_intercepts", bullet_misses);

        connection.send(msg.toString());
        resetEvents();
    }

    // robot collision
    public void onHitRobot(HitRobotEvent event) {
        ++enemy_collisions;
    }

    // we have shot an enemy
    public void onBulletHit(BulletHitEvent event) {

        ++enemy_hits;
    }

    // an enemy has shot us
    public void onHitByBullet(HitByBulletEvent event) {
        ++wounds;
    }

    public void onHitWall(HitWallEvent event) {
        ++wall_collisions;
    }

    public void onBulletMissed(BulletMissedEvent event) {
        ++bullet_misses;
    }

    public void onBulletHitBullet(BulletHitBulletEvent event) {
        ++bullet_intercepts;
    }

    public void onWin(WinEvent event) {
        connection.close();
    }

    public void onBattleEnded(BattleEndedEvent event) {
        connection.close();
    }

    public void onRoundEnded(RoundEndedEvent event) {
        connection.close();
    }

}
