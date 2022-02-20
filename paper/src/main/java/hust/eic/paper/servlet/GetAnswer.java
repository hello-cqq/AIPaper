package hust.eic.paper.servlet;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.springframework.web.context.WebApplicationContext;
import org.springframework.web.context.support.WebApplicationContextUtils;

import hust.eic.paper.teacher.TeacherDAO;

/**
 * Servlet implementation class GetAnswer
 */
@WebServlet("/GetAnswer")
public class GetAnswer extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public GetAnswer() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		response.getWriter().append("Served at: ").append(request.getContextPath());
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
request.setCharacterEncoding("utf-8");
		String courseId = request.getParameter("courseId");
		System.out.println(courseId);
		WebApplicationContext ctx = WebApplicationContextUtils
				.getWebApplicationContext(getServletConfig().getServletContext());
		String msg = ctx.getBean("teacherDAO", TeacherDAO.class).getAnswerJson(courseId);
		response.setContentType("text/html;charset=utf-8");
		response.getWriter().write(msg);
	}

}
