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

    public void run() {

        connection.open();

        while (true) {
            action = proxy.randomAction();
            proxy.execAction(action);

            netSendAction();
        }
    }

    public void xonScannedRobot(ScannedRobotEvent e) {
        distance = e.getDistance();
        proxy.fireAtEnemy(distance);
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
        msg.put("frame", Integer.toString(frame));
        msg.put("battle", Integer.toString(getRoundNum()));
        msg.put("max_battles", Integer.toString(getNumRounds()));
        return msg;
    }

    private void netSendEvent(String event) {
        JSONObject msg = createTrainMsg();
        msg.put("type", "event");
        msg.put("event", event);
        connection.send(msg.toString());
    }

    private void netSendAction() {
        ++frame; // update frame counter for message
        JSONObject msg = createTrainMsg();
        msg.put("type", "action");
        msg.put("action", proxy.actionToString(action));
        msg.put("x", String.format("%f", getX()));
        msg.put("y", String.format("%f", getY()));
        msg.put("distance", String.format("%f", distance));
        msg.put("bearing", String.format("%f", bearing));
        connection.send(msg.toString());
    }

    // robot collision
    public void onHitRobot(HitRobotEvent event) {
        netSendEvent( "HitRobotEvent");
    }

    // we have shot an enemy
    public void onBulletHit(BulletHitEvent event) {

        netSendEvent("BulletHitEvent");
    }

    // an enemy has shot us
    public void onHitByBullet(HitByBulletEvent event) {
        netSendEvent("HitByBulletEvent");
    }

    public void onHitWall(HitWallEvent event) {
        netSendEvent("HitWallEvent");
    }

    public void onBulletMissed(BulletMissedEvent event) {
        netSendEvent("BulletMissedEvent");
    }

    public void onBulletHitBullet(BulletHitBulletEvent event) {
        netSendEvent("BulletHitBulletEvent");
    }

    public void onWin(WinEvent event) {
        netSendEvent("WinEvent");
        connection.close();
    }

    public void onBattleEnded(BattleEndedEvent event) {
        netSendEvent("BattleEndedEvent");
        connection.close();
    }

    public void onRoundEnded(RoundEndedEvent event) {
        netSendEvent("RoundEndedEvent");
        connection.close();
    }

}
