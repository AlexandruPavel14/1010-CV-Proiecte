/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;
import javax.swing.JTable;
import net.proteanit.sql.DbUtils;
import java.sql.DriverManager;

/**
 *
 * @author Alexandru
 */
public class Connecting2DB {
  
    public void delete(String id_persoana)
    {
        Connection con;
        Statement st;
        ResultSet rs;
        String url="jdbc:ucanaccess://C:\\\\Windows\\\\System32\\\\config\\\\systemprofile\\\\Desktop\\\\ProiectPractica-Info2\\\\Practica2.accdb";
        try{
            con=DriverManager.getConnection(url);
            st=con.createStatement();
            String query="DELETE from persoane WHERE id_persoana="+id_persoana;
            int a = st.executeUpdate(query);
        }catch(Exception e)
        {
            System.out.println(e);
        }
        
        
    }
    
}
