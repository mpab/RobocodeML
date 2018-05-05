package Common;

import robocode.AdvancedRobot;
import robocode.Rules;

import java.util.Random;

public class BotProxy {
    public AdvancedRobot bot;
	public static final int NUM_ACTIONS = 5;

    public BotProxy(AdvancedRobot bot) {
        this.bot = bot;
    }

    public int randomAction() {
		java.util.Random rand = new Random();
		// +1 makes range inclusive, 1 -> NUM_ACTIONS
		return rand.nextInt(NUM_ACTIONS) + 1;
	}

	public void fireAtEnemy(double distance) {

		if (bot.getGunHeat() > 0)
			return;

		double scale = (500 - distance) / 500;
		double range = Rules.MAX_BULLET_POWER - Rules.MIN_BULLET_POWER + 1;
		double power = Rules.MIN_BULLET_POWER + scale * range;

		if (power < Rules.MIN_BULLET_POWER)
			power = Rules.MIN_BULLET_POWER;

        if (power > Rules.MAX_BULLET_POWER)
            power = Rules.MAX_BULLET_POWER;

		bot.fire(power);
	}

	public String actionToString(int action) {
        switch (action) {

            case 1:	// stop
                return "STOP";

            case 2:	// forwards
                return "FORWARD";

            case 3:	// backwards
                return "BACK";

            case 4:	// cw
                return "CW";

            case 5:	// ccw
                return "CCW";

            default: // exception
                break;
        }
        return String.format("UNKNOWN ACTION: %d", action);
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
				bot.setTurnRight(90);
				bot.setAhead(150);
				break;

			case 5:	// ccw
				bot.setTurnLeft(90);
				bot.setAhead(150);
				break;

			default: // exception
				bot.out.format("execAction - unhandled state %d\n", action);
		}

        bot.turnGunRight(360);
	}



}
