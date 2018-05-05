package NN;

import Common.Observation;
import org.json.JSONObject;

public class NNTester extends NNTrainer {

    int handshake;

    public void run() {

        conn.open("localhost", 8889);

        obs = new Observation(getRoundNum() + 1, getNumRounds(), 1, -1);
        conn.send(obs.toJson().toString()); // ensure we get an update

        while (true) {
            int action = getNextAction();
            proxy.execAction(action);
            updateObservation();
            conn.send(obs.toJson().toString());
        }
    }

    private void updateObservation() {
        obs.action = -1;
        obs.x = getX();
        obs.y = getY();
        obs.heading = getHeading();
        obs.handshake = handshake;
        obs.frame++;
    }

    private int getNextAction() {
        String msg = conn.receive();
        JSONObject jsn = new JSONObject(msg);
        int action = jsn.getInt("action");
        handshake = jsn.getInt("handshake");
        //System.out.printf("getNextAction() -> %s\n", proxy.actionToString(action));
        return action;
    }


}
