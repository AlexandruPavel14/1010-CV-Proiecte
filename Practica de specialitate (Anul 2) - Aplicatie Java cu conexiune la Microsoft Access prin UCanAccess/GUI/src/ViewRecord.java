/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */

/**
 *
 * @author Alexandru
 */
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;
import javax.swing.JTable;
import net.proteanit.sql.DbUtils;
import java.sql.DriverManager;


public class ViewRecord{

	public void view(JTable table)
	{
		try 
		{
			Connection con = DriverManager.getConnection("jdbc:ucanaccess://C:\\WINDOWS\\System32\\config\\systemprofile\\Desktop\\ProiectPractica-Info2\\Practica2.accdb");

			Statement st = con.createStatement(); 

			String sql = "SELECT * From persoane";
                    
			ResultSet rs = st.executeQuery(sql);
                        
			table.setModel(DbUtils.resultSetToTableModel(rs));
                        
		}
		catch (Exception e)
		{
			System.out.println(e);
		}
	}
}



