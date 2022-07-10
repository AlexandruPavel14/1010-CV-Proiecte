
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import javax.swing.JOptionPane;

/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */

/**
 *
 * @author Alexandru
 */
public class Connecting1DB {
    /*
   public void update (String id_persoana, String CNP, String nume, String prenume,String meserie,String loc_domiciliu)
   {
        Connection con;
        Statement st;
        ResultSet rs;
        String url="jdbc:ucanaccess://C:\\\\Windows\\\\System32\\\\config\\\\systemprofile\\\\Desktop\\\\ProiectPractica-Info2\\\\Practica2.accdb";
       try{
        con=DriverManager.getConnection(url);
        String sql = "UPDATE id_persoana SET CNP = ?, nume = ?, prenume = ?, meserie = ?, loc_domiciliu = ?"+id_persoana;
        PreparedStatement ps=con.prepareStatement(sql);
        ps.setString(0,id_persoana);
        ps.setString(1,CNP);
        ps.setString(2,nume);
        ps.setString(3,prenume);
        ps.setString(4,meserie);
        ps.setString(5,loc_domiciliu);
        ps.executeUpdate();
        ps.close();

       }catch(Exception e)
        {
            System.out.println(e);
        }
   }
*/
    
       public boolean UpdateRecord(int id_persoana, String CNP, String nume, String prenume, int meserie, int loc_domiciliu){
        Connection con;
        
        //Connection con_obj = con;
        Statement st;
        ResultSet rs;
        String url="jdbc:ucanaccess://C:\\\\Windows\\\\System32\\\\config\\\\systemprofile\\\\Desktop\\\\ProiectPractica-Info2\\\\Practica2.accdb";
   
       boolean b = false;
       try{
           con=DriverManager.getConnection(url);
           String update = "UPDATE PERSOANE SeT CNP = '"+CNP+"',nume = '"+nume+"',prenume = '"+prenume+"',meserie = '"+meserie+"',loc_domiciliu = '"+loc_domiciliu+"' WHERE id_persoana = '"+id_persoana+"' ";
           st = con.createStatement();
           int Result = st.executeUpdate(update);
           b = true;
       }catch(Exception ex){
           JOptionPane.showMessageDialog(null,ex);
       }
        return b;
       }
}
