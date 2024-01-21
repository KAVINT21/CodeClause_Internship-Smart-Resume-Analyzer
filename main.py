import openai
import streamlit as st
import base64
import PyPDF2
from io import BytesIO
import re
from streamlit_tags import st_tags
import random
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Smart Resume Analyzer",
    # page_icon='./Logo/SRA_Logo.ico',
)

def course_recommender(course_list,d):
    keywords = st_tags(label='### Certifications that you have',
                       text='See our Certifications recommendation',
                       value=d['certifications'], key='10')
    st.subheader("**Courses & Certificates🎓 Recommendations**")
    c = 0
    rec_course = []
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 4)
    random.shuffle(course_list)
    for c_name, c_link in course_list:
        c += 1
        st.markdown(f"({c}) [{c_name}]({c_link})")
        rec_course.append(c_name)
        if c == no_of_reco:
            break

    # st.subheader("**Projects and Achievements💼**")
    # keywords = st_tags(label='### Projects that you have done',
    #                    text='Add More',
    #                    value=d['projects'], key='7')
    return rec_course


def query_chatgpt(prompt):
    # Define the model name (e.g., "gpt-3.5-turbo")
    model = "gpt-3.5-turbo"

    # Make the API call for chat-based completion
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract and return the generated message from the response
    return response['choices'][0]['message']['content']

def extract_info(pattern, text):
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""


def run():
    st.title("Smart Resume Analyzer")

    pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])

    if pdf_file is not None:
        # Read the PDF file contents using BytesIO
        pdf_contents = pdf_file.read()

        # Use BytesIO to create a file-like object
        pdf_bytesio = BytesIO(pdf_contents)

        pdfReader = PyPDF2.PdfReader(pdf_bytesio)
        pageHandle = pdfReader.pages[0]
        text = pageHandle.extract_text()
        text = text.replace("o", '')
        text = text.replace('|', '')
        print(text)

        # Convert PDF to base64
        pdf_base64 = base64.b64encode(pdf_contents).decode('utf-8')

        st.subheader("**Resume PDF Viewer**")
        # Display PDF
        st.markdown(
            f'<embed src="data:application/pdf;base64,{pdf_base64}" width="700" height="1000" type="application/pdf"></embed>',
            unsafe_allow_html=True)

        openai.api_key = "" #YOUR CHATGPT API KEY



        # Example usage
        user_input = text + " Give the name,contact,email id,certifications,skills,projects he has done"
        resume_text = query_chatgpt(user_input)
        print(resume_text)
        d = {}
        d['name'] = extract_info(r"Name:(.+?)Contact", resume_text)
        d['contact'] = extract_info(r"Contact:(.+?)Email", resume_text)
        d['email'] = extract_info(r"Email:(.+?)Certifications", resume_text)
        d['certifications'] = [cert.strip('- ') for cert in
                               extract_info(r"Certifications:(.+?)Skills", resume_text).split('\n') if cert.strip()]
        d['skills'] = [skill.strip('- ') for skill in extract_info(r"Skills:(.+?)Projects", resume_text).split('\n') if
                       skill.strip()]
        d['projects'] = [re.sub(r'^\d+\.|- ', '', project.strip()) for project in
                         extract_info(r"\d\.(.+?)Education", resume_text).split('\n') if project.strip()]

        if text:
            st.header("**Resume Analysis**")
            st.success("Hello " + d['name'])
            st.subheader("**Your Basic info**")
            try:
                st.text('Name: ' + d['name'])
                st.text('Email: ' + d['email'])
                st.text('Contact: ' + d['contact'])
            except:
                pass
            st.subheader("**Skills Recommendation💡**")
            keywords = st_tags(label='### Skills that you have',
                               text='See our skills recommendation',
                               value=d['skills'], key='1')
            ds_keyword = ['tensorflow', 'keras', 'pytorch', 'machine learning', 'deep Learning', 'flask',
                          'streamlit']
            web_keyword = ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress',
                           'javascript', 'angular js', 'c#', 'flask']
            android_keyword = ['android', 'android development', 'flutter', 'kotlin', 'xml', 'kivy']
            ios_keyword = ['ios', 'ios development', 'swift', 'cocoa', 'cocoa touch', 'xcode']
            uiux_keyword = ['ux', 'adobe xd', 'figma', 'zeplin', 'balsamiq', 'ui', 'prototyping', 'wireframes',
                            'storyframes', 'adobe photoshop', 'photoshop', 'editing', 'adobe illustrator',
                            'illustrator', 'adobe after effects', 'after effects', 'adobe premier pro',
                            'premier pro', 'adobe indesign', 'indesign', 'wireframe', 'solid', 'grasp',
                            'user research', 'user experience']
            web_course = [['Django Crash course [Free]', 'https://youtu.be/e1IyzVyrLSU'],
                          ['Python and Django Full Stack Web Developer Bootcamp',
                           'https://www.udemy.com/course/python-and-django-full-stack-web-developer-bootcamp'],
                          ['React Crash Course [Free]', 'https://youtu.be/Dorf8i6lCuk'],
                          ['ReactJS Project Development Training',
                           'https://www.dotnettricks.com/training/masters-program/reactjs-certification-training'],
                          ['Full Stack Web Developer - MEAN Stack',
                           'https://www.simplilearn.com/full-stack-web-developer-mean-stack-certification-training'],
                          ['Node.js and Express.js [Free]', 'https://youtu.be/Oe421EPjeBE'],
                          ['Flask: Develop Web Applications in Python',
                           'https://www.educative.io/courses/flask-develop-web-applications-in-python'],
                          ['Full Stack Web Developer by Udacity',
                           'https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044'],
                          ['Front End Web Developer by Udacity',
                           'https://www.udacity.com/course/front-end-web-developer-nanodegree--nd0011'],
                          ['Become a React Developer by Udacity',
                           'https://www.udacity.com/course/react-nanodegree--nd019']]

            android_course = [['Android Development for Beginners [Free]', 'https://youtu.be/fis26HvvDII'],
                              ['Android App Development Specialization',
                               'https://www.coursera.org/specializations/android-app-development'],
                              ['Associate Android Developer Certification',
                               'https://grow.google/androiddev/#?modal_active=none'],
                              ['Become an Android Kotlin Developer by Udacity',
                               'https://www.udacity.com/course/android-kotlin-developer-nanodegree--nd940'],
                              ['Android Basics by Google',
                               'https://www.udacity.com/course/android-basics-nanodegree-by-google--nd803'],
                              ['The Complete Android Developer Course',
                               'https://www.udemy.com/course/complete-android-n-developer-course/'],
                              ['Building an Android App with Architecture Components',
                               'https://www.linkedin.com/learning/building-an-android-app-with-architecture-components'],
                              ['Android App Development Masterclass using Kotlin',
                               'https://www.udemy.com/course/android-oreo-kotlin-app-masterclass/'],
                              ['Flutter & Dart - The Complete Flutter App Development Course',
                               'https://www.udemy.com/course/flutter-dart-the-complete-flutter-app-development-course/'],
                              ['Flutter App Development Course [Free]', 'https://youtu.be/rZLR5olMR64']]

            ios_course = [
                ['IOS App Development by LinkedIn', 'https://www.linkedin.com/learning/subscription/topics/ios'],
                ['iOS & Swift - The Complete iOS App Development Bootcamp',
                 'https://www.udemy.com/course/ios-13-app-development-bootcamp/'],
                ['Become an iOS Developer', 'https://www.udacity.com/course/ios-developer-nanodegree--nd003'],
                ['iOS App Development with Swift Specialization',
                 'https://www.coursera.org/specializations/app-development'],
                ['Mobile App Development with Swift',
                 'https://www.edx.org/professional-certificate/curtinx-mobile-app-development-with-swift'],
                ['Swift Course by LinkedIn', 'https://www.linkedin.com/learning/subscription/topics/swift-2'],
                ['Objective-C Crash Course for Swift Developers', 'https://www.udemy.com/course/objectivec/'],
                ['Learn Swift by Codecademy', 'https://www.codecademy.com/learn/learn-swift'],
                ['Swift Tutorial - Full Course for Beginners [Free]', 'https://youtu.be/comQ1-x2a1Q'],
                ['Learn Swift Fast - [Free]', 'https://youtu.be/FcsY1YPBwzQ']]
            uiux_course = [['Google UX Design Professional Certificate',
                            'https://www.coursera.org/professional-certificates/google-ux-design'],
                           ['UI / UX Design Specialization', 'https://www.coursera.org/specializations/ui-ux-design'],
                           ['The Complete App Design Course - UX, UI and Design Thinking',
                            'https://www.udemy.com/course/the-complete-app-design-course-ux-and-ui-design/'],
                           ['UX & Web Design Master Course: Strategy, Design, Development',
                            'https://www.udemy.com/course/ux-web-design-master-course-strategy-design-development/'],
                           ['The Complete App Design Course - UX, UI and Design Thinking',
                            'https://www.udemy.com/course/the-complete-app-design-course-ux-and-ui-design/'],
                           ['DESIGN RULES: Principles + Practices for Great UI Design',
                            'https://www.udemy.com/course/design-rules/'],
                           ['Become a UX Designer by Udacity',
                            'https://www.udacity.com/course/ux-designer-nanodegree--nd578'],
                           ['Adobe XD Tutorial: User Experience Design Course [Free]', 'https://youtu.be/68w2VwalD5w'],
                           ['Adobe XD for Beginners [Free]', 'https://youtu.be/WEljsc2jorI'],
                           ['Adobe XD in Simple Way', 'https://learnux.io/course/adobe-xd']]

            st.subheader("**Personality Trait Analysis**")
            user = resume_text + " Analyse these traits and give its percentage levels.(Analytical Thinking,Creativity,Problem-Solving,Adaptability,Leadership,Communication,Attetion to Detail,Time Management)"
            response = query_chatgpt(user)
            print(response)
            seeds = ["Analytical Thinking", "Creativity", "Problem-Solving", "Adaptability", "Leadership",
                     "Communication", "Attention To Detail", "Time Management"]
            trait_levels = {}
            i = 0
            j = 0
            while i < len(response):
                if response[i].isdigit() and response[i + 1].isdigit():
                    trait_levels[seeds[j]] = response[i:i + 2]
                    j = j + 1
                    i = i + 2
                    continue
                i = i + 1
            df = pd.DataFrame(list(trait_levels.items()), columns=['trait', 'percentile'])
            df['percentile'] = df['percentile'].astype(int)

            # Create a bar chart using Seaborn
            plt.figure(figsize=(15, 5))
            sns.barplot(x='percentile', y='trait', data=df, palette='viridis')
            plt.title('Trait Analysis')
            plt.xlabel('Percentage Level')
            plt.ylabel('Trait')

            # Display the plot in Streamlit
            st.pyplot(plt)
            df = pd.DataFrame(list(trait_levels.items()), columns=['Trait', 'Score'])
            df['Score'] = df['Score'].astype(int)

            # Create a donut plot
            fig, ax = plt.subplots(figsize=(4, 4))
            ax.pie(df['Score'], labels=df['Trait'], autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.4),
                   colors=sns.color_palette('viridis'))

            # Draw a circle at the center to create a donut plot
            centre_circle = plt.Circle((0, 0), 0.6, fc='white')
            fig = plt.gcf()
            fig.gca().add_artist(centre_circle)

            # Equal aspect ratio ensures that the pie is drawn as a circle
            ax.axis('equal')
            plt.title('Trait Analysis')

            st.pyplot(plt)
            df = pd.DataFrame(list(trait_levels.items()), columns=['Trait', 'Percentile'])

            # Create a line plot
            plt.figure(figsize=(10, 6))
            line_plot, = plt.plot(df['Trait'], df['Percentile'], marker='o', color='orange', label='Trait Percentile')
            plt.title('Trait Analysis - Line Plot')
            plt.xlabel('Trait')
            plt.ylabel('Percentage Level')
            plt.legend()
            st.pyplot(line_plot.figure)
            recommended_skills = []
            reco_field = ''
            rec_course = ''
            for i in d['skills']:
                ## Data science recommendation
                if i.lower() in ds_keyword:
                    print(i.lower())
                    reco_field = 'Data Science'
                    st.success("** Our analysis says you are looking for Data Science Jobs.**")
                    recommended_skills = ['Data Visualization', 'Predictive Analysis', 'Statistical Modeling',
                                          'Data Mining', 'Clustering & Classification', 'Data Analytics',
                                          'Quantitative Analysis', 'Web Scraping', 'ML Algorithms', 'Keras',
                                          'Pytorch', 'Probability', 'Scikit-learn', 'Tensorflow', "Flask",
                                          'Streamlit']
                    recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                   text='Recommended skills generated from System',
                                                   value=recommended_skills, key='2')
                    st.markdown(
                        '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                        unsafe_allow_html=True)
                    ds_course = [['Machine Learning Crash Course by Google [Free]',
                                  'https://developers.google.com/machine-learning/crash-course'],
                                 ['Machine Learning A-Z by Udemy', 'https://www.udemy.com/course/machinelearning/'],
                                 ['Machine Learning by Andrew NG', 'https://www.coursera.org/learn/machine-learning'],
                                 ['Data Scientist Master Program of Simplilearn (IBM)',
                                  'https://www.simplilearn.com/big-data-and-analytics/senior-data-scientist-masters-program-training'],
                                 ['Data Science Foundations: Fundamentals by LinkedIn',
                                  'https://www.linkedin.com/learning/data-science-foundations-fundamentals-5'],
                                 ['Data Scientist with Python',
                                  'https://www.datacamp.com/tracks/data-scientist-with-python'],
                                 ['Programming for Data Science with Python',
                                  'https://www.udacity.com/course/programming-for-data-science-nanodegree--nd104'],
                                 ['Programming for Data Science with R',
                                  'https://www.udacity.com/course/programming-for-data-science-nanodegree-with-R--nd118'],
                                 ['Introduction to Data Science',
                                  'https://www.udacity.com/course/introduction-to-data-science--cd0017'],
                                 ['Intro to Machine Learning with TensorFlow',
                                  'https://www.udacity.com/course/intro-to-machine-learning-with-tensorflow-nanodegree--nd230']]

                    rec_course = course_recommender(ds_course,d)
                    break

                ## Web development recommendation
                elif i.lower() in web_keyword:
                    print(i.lower())
                    reco_field = 'Web Development'
                    st.success("** Our analysis says you are looking for Web Development Jobs **")
                    recommended_skills = ['React', 'Django', 'Node JS', 'React JS', 'php', 'laravel', 'Magento',
                                          'wordpress', 'Javascript', 'Angular JS', 'c#', 'Flask', 'SDK']
                    recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                   text='Recommended skills generated from System',
                                                   value=recommended_skills, key='3')
                    st.markdown(
                        '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                        unsafe_allow_html=True)
                    rec_course = course_recommender(web_course,d)

                    break

                ## Android App Development
                elif i.lower() in android_keyword:
                    print(i.lower())
                    reco_field = 'Android Development'
                    st.success("** Our analysis says you are looking for Android App Development Jobs **")
                    recommended_skills = ['Android', 'Android development', 'Flutter', 'Kotlin', 'XML', 'Java',
                                          'Kivy', 'GIT', 'SDK', 'SQLite']
                    recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                   text='Recommended skills generated from System',
                                                   value=recommended_skills, key='4')
                    st.markdown(
                        '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                        unsafe_allow_html=True)
                    rec_course = course_recommender(android_course,d)
                    break

                ## IOS App Development
                elif i.lower() in ios_keyword:
                    print(i.lower())
                    reco_field = 'IOS Development'
                    st.success("** Our analysis says you are looking for IOS App Development Jobs **")
                    recommended_skills = ['IOS', 'IOS Development', 'Swift', 'Cocoa', 'Cocoa Touch', 'Xcode',
                                          'Objective-C', 'SQLite', 'Plist', 'StoreKit', "UI-Kit", 'AV Foundation',
                                          'Auto-Layout']
                    recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                   text='Recommended skills generated from System',
                                                   value=recommended_skills, key='5')
                    st.markdown(
                        '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                        unsafe_allow_html=True)
                    rec_course = course_recommender(ios_course,d)
                    break

                ## Ui-UX Recommendation
                elif i.lower() in uiux_keyword:
                    print(i.lower())
                    reco_field = 'UI-UX Development'
                    st.success("** Our analysis says you are looking for UI-UX Development Jobs **")
                    recommended_skills = ['UI', 'User Experience', 'Adobe XD', 'Figma', 'Zeplin', 'Balsamiq',
                                          'Prototyping', 'Wireframes', 'Storyframes', 'Adobe Photoshop', 'Editing',
                                          'Illustrator', 'After Effects', 'Premier Pro', 'Indesign', 'Wireframe',
                                          'Solid', 'Grasp', 'User Research']
                    recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                   text='Recommended skills generated from System',
                                                   value=recommended_skills, key='6')
                    st.markdown(
                        '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                        unsafe_allow_html=True)

                    rec_course = course_recommender(uiux_course,d)
                    break

    else:
        st.warning("Please upload a PDF file.")

run()
