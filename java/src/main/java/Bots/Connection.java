package Bots;

import java.io.DataInputStream;
import java.io.DataOutputStream;
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
                close();
            }
        }
    }

    public String receive() {

        if (status == 1) {
            try {
                DataInputStream dis = new DataInputStream(socket.getInputStream());
                return dis.readUTF();
            } catch (Exception e) {
                System.out.println(e);
                close();
            }
        }

        return null;
    }

}
