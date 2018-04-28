package Bots;

import org.json.JSONObject;
import robocode.*;

public class Trainer extends AdvancedRobot {

    private BotProxy proxy = new BotProxy(this);
    Connection connection = new Connection();

    int frame = 0;

    // features
    int action;
    double enemy_distance;
    double enemy_bearing;
    // plus x, y

    // events
    int enemy_collisions;
    int wall_collisions;
    int shell_hits;
    int shell_wounds;
    int shell_misses;
    int shell_intercepts;

    public void run() {

        connection.open();

        while (true) {
            action = proxy.randomAction();
            netUpdate();
            proxy.execAction(action);
        }
    }

    private void resetEvents() {
        enemy_collisions = 0;
        wall_collisions = 0;
        shell_hits = 0;
        shell_wounds = 0;
        shell_misses = 0;
        shell_intercepts = 0;
    }

    public void onScannedRobot(ScannedRobotEvent e) {

        enemy_distance = e.getDistance();

        double lastEnemyBearing = e.getBearing() % 360;

        // Calculate the angle to the scanned robot
        double angle = Math.toRadians((getHeading() + lastEnemyBearing));
        double enemyX = getX() + Math.sin(angle) * enemy_distance;
        double enemyY = getY() + Math.cos(angle) * enemy_distance;

        //absolute angle to enemy
        enemy_bearing = Util.absBearing(
                (float)getX(),
                (float)getY(),
                (float)enemyX,
                (float)enemyY);

        proxy.fireAtEnemy(enemy_distance);
    }

    private JSONObject createTrainMsg() {
        ++frame; // update frame counter for message
        JSONObject msg = new JSONObject();
        msg.put("round", getRoundNum() + 1);
        msg.put("num_rounds", getNumRounds());
        msg.put("frame", frame);
        return msg;
    }

    private void netUpdate() {
        JSONObject msg = createTrainMsg();

        // features
        msg.put("action", action);
        msg.put("x", getX());
        msg.put("y", getY());
        msg.put("heading", getHeading());
        msg.put("enemy_distance", enemy_distance);
        msg.put("enemy_bearing", enemy_bearing);

        // events
        msg.put("enemy_collisions", enemy_collisions);
        msg.put("wall_collisions", wall_collisions);
        msg.put("shell_hits", shell_hits);
        msg.put("shell_wounds", shell_wounds);
        msg.put("shell_misses", shell_misses);
        msg.put("shell_intercepts", shell_misses);

        connection.send(msg.toString());
        resetEvents();
    }

    // robot collision
    public void onHitRobot(HitRobotEvent event) {
        ++enemy_collisions;
    }

    // we have shot an enemy
    public void onBulletHit(BulletHitEvent event) {

        ++shell_hits;
    }

    // an enemy has shot us
    public void onHitByBullet(HitByBulletEvent event) {
        ++shell_wounds;
    }

    public void onHitWall(HitWallEvent event) {
        ++wall_collisions;
    }

    public void onBulletMissed(BulletMissedEvent event) {
        ++shell_misses;
    }

    public void onBulletHitBullet(BulletHitBulletEvent event) {
        ++shell_intercepts;
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
