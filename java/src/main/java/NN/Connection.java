package NN;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.net.Socket;

public class Connection {

    protected Socket socket;
    protected int status; // 0 = closed, 1 = open, -1 = error

    public void open(String host, int port) {

        if (status == 1)
            return;

        try {
            socket = new Socket(host, port);
            status = 1;
        } catch(Exception e) {
            System.out.println(e);
            status = -1;
        }
    }

    public void close() {

        if (status == 0)
            return;

        try {
            socket.close();
            status = 0;
        } catch(Exception e) {
            System.out.println(e);
            status = -1;
        }
    }

    public void send(String msg) {
        if (status == 1) {
            try {
                DataOutputStream out = new DataOutputStream(socket.getOutputStream());
                out.writeBytes(msg);
                out.flush();
            } catch (Exception e) {
                System.out.println(e);
                status = -1;
            }

            if (status == -1) {
                try {
                    socket.close();
                } catch(Exception e) {
                    System.out.println(e);
                }
            }
        }
    }

    public String receive() {

        if (status == 1) {
            try {
                BufferedReader br = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                String msg = br.readLine();
                return msg;
            } catch (Exception e) {
                System.out.println(e);
                status = -1;
            }
        }

        if (status == -1) {
            try {
                socket.close();
            } catch(Exception e) {
                System.out.println(e);
            }
        }

        return null;
    }

}
