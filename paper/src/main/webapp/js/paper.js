var currentTerm = function(){
	year = new Date().getFullYear();
	month = new Date().getMonth()+1;
//	return month>2&&month<9 ? year+'年春季':year+'年秋季';
	return '2018年秋季';
}
var teacher = function(){
	var t = {
		name:'徐晶',
		num:'T666666'	,
		// disabled:true
	};
	return t;
}
var uploadedImgNums = 0;
var app = new Vue({
	el:"#app",
	data:{
		term:currentTerm(),
		teacherNum:teacher().num,
		termCourses:[],
		courseId:'',
		teacher:teacher(),
		students:[],
		answer:null,
		dialogImageUrl: '',
        dialogVisible: false,
		fileList: [],
		imgUploadPath:{
			imgPath:''
		},
		currentCorrectedStudent:null,
		correctedIndex:0
	},
	methods:{
		correctPaper:function(index,row){
			this.currentCorrectedStudent = row;
			console.log('ccs:',this.currentCorrectedStudent);
			let $table = this.$refs.table;
		    this.students.map((item) => {
				$table.toggleRowExpansion(item, false)
		    });
		    $table.toggleRowExpansion(row);
			this.correctedIndex = index;
		},
		giveScore:function(value){
			this.currentCorrectedStudent.grade.judge.grade = 0;
			this.currentCorrectedStudent.grade.q_short.grade = 0;
			this.currentCorrectedStudent.grade.q_compute.grade = 0;
			for(i in this.currentCorrectedStudent.grade.judge.goal){
				this.currentCorrectedStudent.grade.judge.grade+=this.currentCorrectedStudent.grade.judge.goal[i];
			}
			for(i in this.currentCorrectedStudent.grade.q_short.goal){
				this.currentCorrectedStudent.grade.q_short.grade+=this.currentCorrectedStudent.grade.q_short.goal[i];
			}
			for(i in this.currentCorrectedStudent.grade.q_compute.answer){
				this.currentCorrectedStudent.grade.q_compute.grade+=this.currentCorrectedStudent.grade.q_compute.answer[i].goal;
			}
			
			this.currentCorrectedStudent.grade.total = (Number)((this.currentCorrectedStudent.grade.choice.grade+this.currentCorrectedStudent.grade.judge.grade+this.currentCorrectedStudent.grade.q_short.grade+this.currentCorrectedStudent.grade.q_compute.grade).toFixed(1));
			this.currentCorrectedStudent.grade.judge.grade = (Number)(this.currentCorrectedStudent.grade.judge.grade.toFixed(1));
			this.currentCorrectedStudent.grade.q_short.grade = (Number)(this.currentCorrectedStudent.grade.q_short.grade.toFixed(1));
			this.currentCorrectedStudent.grade.q_compute.grade = (Number)(this.currentCorrectedStudent.grade.q_compute.grade.toFixed(1));
		},
		closePand:function(index,row){
			let $table = this.$refs.table;
			$table.toggleRowExpansion(row,false);
		},
		listStudents:function(){
			this.$http.post('/paper/GetAnswer',{courseId:this.courseId},{emulateJSON:true}).then(function(res){
				if(res.bodyText.length!=0)
					this.answer = JSON.parse(res.bodyText);
				console.log(this.answer);
			},function(res){
			    console.log(res.status);
			});
			this.$http.post('/paper/GetStudents',{courseId:this.courseId,teacherNum:this.teacherNum},{emulateJSON:true}).then(function(res){
				this.students = JSON.parse(res.bodyText);
				console.log(this.students);
			},function(res){
			    console.log(res.status);
			});
			this.imgUploadPath.imgPath = this.term+'/'+this.getCourseName()+'/'+this.teacher.name;
		},
		getCourseName:function(){
			for(i in this.termCourses){
				if(this.termCourses[i].id+'' == this.courseId){			
					return this.termCourses[i].name;
				}
			}
		},
		submitGrade:function(){
			thisStudent = JSON.stringify(this.currentCorrectedStudent);
			console.log(thisStudent);
			this.$http.post('/paper/SubmitGrade',{courseId:this.courseId,teacherNum:this.teacherNum,student:thisStudent},{emulateJSON:true}).then(function(res){
				document.getElementsByClassName('el-icon-success')[this.correctedIndex].style.display="";
			},function(res){
			    console.log(res.status);
			});
		},
		submitUpload:function() {
			if(this.courseId==''){
				this.$message({
					message: '请先选择课程',
					type: 'warning'
				});
			}
			else if(this.$refs.upload.uploadFiles.length%4!=0){
				this.$message({
					message: '图片数量不符合要求',
					type: 'warning'
				});
			}
			else{
				this.$refs.upload.submit();
			}
			
		},
		uploadSuccess:function(response, file, fileList){
			console.log(response,file);
			++uploadedImgNums;
			if(uploadedImgNums==fileList.length){
				// /paperProcess/startImgProcess
				this.$http.post('http://localhost:8000/startImgProcess',{uploadPath:this.imgUploadPath.imgPath,courseId:this.courseId,teacherNum:this.teacherNum},{emulateJSON:true}).then(function(res){
					// this.students = JSON.parse(res.bodyText);
					console.log(JSON.parse(res.bodyText));
					console.log('识别完成');
					this.$message({
						message: '自动识别已完成',
						type: 'success',
						showClose:true,
						duration:5000
					});
					this.listStudents();
				},function(res){
					console.log(res.status);
				});
			}		
		},
		uploadError:function(err, file, fileList){
			console.log(err,file,fileList);
		},
		deleteAllImg:function(){
			this.fileList = [];
			uploadedImgNums = 0;
		},
		handleRemove:function(file, fileList) {
			// console.log(file, fileList);
		},
		handlePreview:function(file) {
			this.dialogImageUrl = file.url;
			this.dialogVisible = true;
		},
		getTotal:function(g){
			console.log(g);
			if (g==-1) {
				return '未录入';
			} else{
				return g;
			}
		}
	},
	mounted:function(){
		this.$http.post('/paper/GetTermCourse',{term:this.term},{emulateJSON:true}).then(function(res){
			this.termCourses = JSON.parse(res.bodyText);
			console.log(this.termCourses);
        },function(res){
            console.log(res.status);
        });
	}
});

