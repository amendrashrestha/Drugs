package model;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author amendrashrestha
 */
public class Database {

    public static List<String> getPost(String tableName) {
        List<String> posts = new ArrayList();
        try {
            Connection connection = Connect.getConn();
            String sizeQuery = "SET group_concat_max_len = 1000000000;";

            String selectQuery = "SELECT Post from " + tableName + " where language = " + "\'en" + "\';";

            Statement statement = connection.createStatement();
            statement.execute(sizeQuery);
            ResultSet result = statement.executeQuery(selectQuery);
            while (result.next()) {
                String post = result.getString("Post");
                posts.add(post);
            }
        } catch (SQLException | ClassNotFoundException ex) {
            Logger.getLogger(Database.class.getName()).log(Level.SEVERE, null, ex);
        } catch (InstantiationException | IllegalAccessException ex) {
            Logger.getLogger(Database.class.getName()).log(Level.SEVERE, null, ex);
        }
        return posts;
    }
    
    public static List<String> getAltMediaPost(String tableName) {
        List<String> posts = new ArrayList();
        try {
            Connection connection = Connect.getConn();
            String sizeQuery = "SET group_concat_max_len = 100000000000;";

            String selectQuery = "SELECT News from " + tableName;

            Statement statement = connection.createStatement();
            statement.execute(sizeQuery);
            ResultSet result = statement.executeQuery(selectQuery);
            while (result.next()) {
                String post = result.getString("News");
                posts.add(post);
            }
        } catch (SQLException | ClassNotFoundException ex) {
            Logger.getLogger(Database.class.getName()).log(Level.SEVERE, null, ex);
        } catch (InstantiationException | IllegalAccessException ex) {
            Logger.getLogger(Database.class.getName()).log(Level.SEVERE, null, ex);
        }
        return posts;
    }

}
