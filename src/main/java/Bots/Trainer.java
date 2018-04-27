package Bots;

import robocode.*;

public class Trainer extends AdvancedRobot {

    private BotProxy proxy = new BotProxy(this, new Connection());

    public void run() {
        while (true) {
            proxy.learn();
        }
    }

    public void onScannedRobot(ScannedRobotEvent e) {
        proxy.onScannedRobot(e);
    }

    // robot collision
    public void onHitRobot(HitRobotEvent event) {
        proxy.onHitRobot();
    }

    // we have shot an enemy
    public void onBulletHit(BulletHitEvent event) {
        proxy.onBulletHit();
    }

    // an enemy has shot us
    public void onHitByBullet(HitByBulletEvent event) {
        proxy.onHitByBullet();
    }

    // an enemy has shot us
    public void onHitWall(HitWallEvent event) {
        proxy.onHitWall();
    }

    public void onBulletMissed(BulletMissedEvent event) {
        proxy.onBulletMissed();
    }

    public void onBulletHitBullet(BulletHitBulletEvent event) {
        proxy.onBulletHitBullet();
    }

    public void onWin(WinEvent event) {
        proxy.onWin();
    }

    public void onBattleEnded(BattleEndedEvent event) {
        proxy.onBattleEnded();
    }

    public void onRoundEnded(RoundEndedEvent event) {
        proxy.onRoundEnded();
    }

}
