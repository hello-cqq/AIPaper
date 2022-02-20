package hust.eic.paper.teacher;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

import javax.sql.DataSource;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;

import hust.eic.paper.Paper;
import hust.eic.paper.course.Course;
import hust.eic.paper.student.Grade;
import hust.eic.paper.student.Student;


public class TeacherDAO {

	private DataSource dataSource;

	public void setDataSource(DataSource dataSource) {
		this.dataSource = dataSource;
	}
	public String getTermCoursesJson(String term) {
		String jsonData = "";
		List<Course> courses = new ArrayList<Course>();
		String sql = "select * from courses where term=?";
		Connection conn = null;
		try {
			conn = dataSource.getConnection();
			PreparedStatement ps = conn.prepareStatement(sql);
			ps.setString(1, term);
			ResultSet rs = ps.executeQuery();
			while (rs.next()) {
				Course c = new Course(rs.getInt("id"),rs.getString("name"),rs.getString("term"));
				courses.add(c);
			}
			rs.close();
			ps.close();
			jsonData = JSON.toJSONString(courses);
		} catch (SQLException e) {
			throw new RuntimeException(e);
		} finally {
			if (conn != null) {
				try {
					conn.close();
				} catch (SQLException e) {
				}
			}
		}
		return jsonData;
	}
	
	public String getStudentsJson(String courseId,String teacherNum) {
		String jsonData = "";
		String sql = "select name,num,class,gradeId from all_courses,students where courseId=? and teacherNum=? and all_courses.studentNum=students.num";
		Connection conn = null;
		List<Student> students = new ArrayList<Student>();
		try {
			conn = dataSource.getConnection();
			PreparedStatement ps = conn.prepareStatement(sql);
			ps.setString(1, courseId);
			ps.setString(2, teacherNum);
			ResultSet rs = ps.executeQuery();
			while (rs.next()) {
				int gradeId = rs.getInt("gradeId");
				Grade g = null;
				if(gradeId==-1) {
					g = new Grade(-1,null,null,null,null,null);
					
				}
				else {
					g = getGrade(conn, gradeId);
				}
				Student student = new Student(rs.getString("num"), rs.getString("name"), rs.getString("class"), g);
				students.add(student);
				
			}
			rs.close();
			ps.close();
		} catch (SQLException e) {
			throw new RuntimeException(e);
		} finally {
			if (conn != null) {
				try {
					conn.close();
				} catch (SQLException e) {
				}
			}
		}
		jsonData = JSON.toJSONString(students);
		return jsonData;
	}
	
	public String saveWholeGrade(String courseId,String teacherNum,String student) {
		JSONObject thisStudent = JSON.parseObject(student);
		JSONObject thisGrade = thisStudent.getJSONObject("grade");
		String jsonData = "{'status':'success'}";
		Connection conn = null;
		try {
			
			conn = dataSource.getConnection();
			PreparedStatement ps = null;
			ResultSet rs = null;
			String sql = "select gradeId from all_courses where courseId=? and teacherNum=? and studentNum=?";
			ps = conn.prepareStatement(sql);
			ps.setString(1, courseId);
			ps.setString(2, teacherNum);
			ps.setString(3, thisStudent.getString("num"));
			rs = ps.executeQuery();
			if (rs.next()) {
				int gradeId = rs.getInt("gradeId");
				String sql1 = "update grades set total=?,choice=?,fill=?,judge=?,short=?,compute=? where id=?";
				PreparedStatement ps1 = conn.prepareStatement(sql1);
				ps1.setDouble(1, thisGrade.getDouble("total"));
				ps1.setString(2, JSON.toJSONString(thisGrade.getJSONObject("choice")));
				ps1.setString(3, JSON.toJSONString(thisGrade.getJSONObject("fill")));
				ps1.setString(4, JSON.toJSONString(thisGrade.getJSONObject("judge")));
				ps1.setString(5, JSON.toJSONString(thisGrade.getJSONObject("q_short")));
				ps1.setString(6, JSON.toJSONString(thisGrade.getJSONObject("q_compute")));
				ps1.setInt(7, gradeId);
				ps1.executeUpdate();
				ps1.close();
			}
			rs.close();
			ps.close();
		} catch (SQLException e) {
			throw new RuntimeException(e);
		} finally {
			if (conn != null) {
				try {
					conn.close();
				} catch (SQLException e) {
				}
			}
		}
		return jsonData;
	}
	
	
	public String saveAIGrades(String courseId,String teacherNum,String grades) {
		JSONArray all_grades = JSON.parseArray(grades);
		JSONObject answer = JSONObject.parseObject(getAnswerJson(courseId));
		String jsonData = "{'status':'success'}";
		Connection conn = null;
		try {
			
			conn = dataSource.getConnection();
			for (int i = 0; i < all_grades.size(); i++) {
				PreparedStatement ps = null;
				ResultSet rs = null;
				String sql = "select gradeId from all_courses where courseId=? and teacherNum=? and studentNum=?";
				ps = conn.prepareStatement(sql);
				ps.setString(1, courseId);
				ps.setString(2, teacherNum);
				ps.setString(3, all_grades.getJSONObject(i).getString("stu_num"));
				rs = ps.executeQuery();
				if (rs.next()) {
					int gradeId = rs.getInt("gradeId");
					if(gradeId==-1) {
						gradeId = insertGradeRow(all_grades.getJSONObject(i), answer,conn);
						String sql1 = "update all_courses set gradeId=? where courseId=? and teacherNum=? and studentNum=?";
						PreparedStatement ps1 = conn.prepareStatement(sql1);
						ps1.setInt(1, gradeId);
						ps1.setString(2, courseId);
						ps1.setString(3, teacherNum);
						ps1.setString(4, all_grades.getJSONObject(i).getString("stu_num"));
						ps1.executeUpdate();
						ps1.close();
					}
				}
				rs.close();
				ps.close();
			}
		} catch (SQLException e) {
			throw new RuntimeException(e);
		} finally {
			if (conn != null) {
				try {
					conn.close();
				} catch (SQLException e) {
				}
			}
		}
		return jsonData;
	}
	private int insertGradeRow(JSONObject grade,JSONObject answer,Connection conn) {
		int id = 0;
		
		double grade_total = 0;
		
		JSONArray choice_ans = grade.getJSONArray("choice_ans");
		JSONObject choice = answer.getJSONObject("choice");
		int per_score = choice.getInteger("total")/choice.getInteger("num");
		int[] choice_goal = new int[choice_ans.size()];
		int choice_garde = 0;
		for (int i = 0; i < choice_goal.length; i++) {
			choice_goal[i] = choice_ans.getString(i).equals(choice.getJSONArray("answer").getString(i)) ? per_score:0;
			grade_total+=choice_goal[i];
			choice_garde+=choice_goal[i];
		}
		String grade_choice = JSON.toJSONString(new Choice(choice_goal, choice_ans,choice_garde));
		
		String grade_fill = "{\"grade\": \"нч\", \"answer\": 0}";
		
		JSONObject judge = answer.getJSONObject("judge");
		double[] judge_goal = new double[judge.getInteger("num")];
		double judge_grade = 0;
		String judge_answer = grade.getString("judge_ans");
		String grade_judge = JSON.toJSONString(new Judge(judge_goal, judge_grade, judge_answer));
		
		JSONObject q_short = answer.getJSONObject("q_short");
		double[] short_goal = new double[q_short.getInteger("num")];
		double short_grade = 0;
		String short_answer = grade.getString("short_ans");
		String grade_short = JSON.toJSONString(new QShort(short_goal, short_grade, short_answer));

		double compute_grade = 0;
		List<ComputeAns> cans = new ArrayList<ComputeAns>();
		JSONArray compute_ans = grade.getJSONArray("compute_ans");
		for (int i = 0; i < compute_ans.size(); i++) {
			ComputeAns c = new ComputeAns(0, compute_ans.getString(i));
			cans.add(c);
		}
		String grade_compute = JSON.toJSONString(new QCompute(compute_grade,cans));
		String sql = "insert into grades (total,choice,fill,judge,short,compute) values (?,?,?,?,?,?)";
		PreparedStatement ps = null;
		ResultSet rs = null;
		try {
			ps = conn.prepareStatement(sql,Statement.RETURN_GENERATED_KEYS);
			ps.setDouble(1, grade_total);
			ps.setString(2, grade_choice);
			ps.setString(3, grade_fill);
			ps.setString(4, grade_judge);
			ps.setString(5, grade_short);
			ps.setString(6, grade_compute);
			ps.executeUpdate();
			rs = ps.getGeneratedKeys();
			if(rs.next())
				id = rs.getInt(1);
			rs.close();
			ps.close();
		} catch (SQLException e) {
			throw new RuntimeException(e);
		}
		return id;
	}
	public String getAnswerJson(String courseId) {
		String jsonData = "";
		String sql = "select * from papers where courseId=?";
		Connection conn = null;
		try {
			conn = dataSource.getConnection();
			PreparedStatement ps = conn.prepareStatement(sql);
			ps.setString(1, courseId);
			ResultSet rs = ps.executeQuery();
			if(rs.next()) {
				JSONObject choice = JSON.parseObject(rs.getString("choice"));
				JSONObject fill = JSON.parseObject(rs.getString("fill"));
				JSONObject judge = JSON.parseObject(rs.getString("judge"));
				JSONObject q_short = JSON.parseObject(rs.getString("short"));
				JSONObject q_compute = JSON.parseObject(rs.getString("compute"));
				int total = rs.getInt("total");
				Paper p = new Paper(Integer.parseInt(courseId),total,choice,fill,judge,q_short,q_compute);
				jsonData = JSON.toJSONString(p);
			}
			rs.close();
			ps.close();
			
		} catch (SQLException e) {
			throw new RuntimeException(e);
		} finally {
			if (conn != null) {
				try {
					conn.close();
				} catch (SQLException e) {
				}
			}
		}
		return jsonData;
	}
	private Grade getGrade(Connection conn,int gradeId) {
		Grade g = null;
		String sql = "select * from grades where id=?";
		try {
			PreparedStatement ps = conn.prepareStatement(sql);
			ps.setInt(1, gradeId);
			ResultSet rs = ps.executeQuery();
			if(rs.next()) {
				JSONObject choice = JSON.parseObject(rs.getString("choice"));
				JSONObject fill = JSON.parseObject(rs.getString("fill"));
				JSONObject judge = JSON.parseObject(rs.getString("judge"));
				JSONObject q_short = JSON.parseObject(rs.getString("short"));
				JSONObject q_compute = JSON.parseObject(rs.getString("compute"));
				g = new Grade(rs.getDouble("total"),choice,fill,judge,q_short,q_compute);	
			}
			rs.close();
			ps.close();
		} catch (SQLException e) {
			throw new RuntimeException(e);
		}
		return g;
	}
}
