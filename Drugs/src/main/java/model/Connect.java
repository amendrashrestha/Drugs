package model;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author amendrashrestha
 */
public class Connect {

    public static Connection getConn() throws ClassNotFoundException,
            InstantiationException, IllegalAccessException {
        Connection conn = null;
        String unicode = "?useUnicode=yes&characterEncoding=UTF-8";
        String connect = "&autoReconnect=true&failOverReadOnly=false&maxReconnects=50";
        String db_url = "jdbc:mysql://127.0.0.1:3306/AlternativeMedia";
        String db_username = "root";
        String db_password = "root86";
        
        try {
            Class.forName("com.mysql.jdbc.Driver").newInstance();
            conn = DriverManager.getConnection(db_url+unicode+connect,
                    db_username, db_password);
        } catch (SQLException ex) {
            Logger.getLogger(Connect.class.getName()).log(Level.SEVERE, null, ex);
        }
        return conn;
    }

}
