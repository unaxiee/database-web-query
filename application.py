from flask import Flask, render_template, request
import mysql.connector
import psycopg2
import datetime

application = Flask(__name__)

@application.route("/", methods=['GET', 'POST'])
def home_page():
    try:
        if (request.method == 'POST'):
            if (request.form['database'] == 'mysql'):
                if (request.form['dataset'] == 'instacart_normalized'):
                    connection = mysql.connector.connect(host='mysql2021.c7wtal8gxuuf.us-east-2.rds.amazonaws.com',
                                                         database='instacart_normalized',
                                                         user='mysql2021',
                                                         password='mysql2021')
                elif (request.form['dataset'] == 'instacart'):
                    connection = mysql.connector.connect(host='mysql2021.c7wtal8gxuuf.us-east-2.rds.amazonaws.com',
                                                         database='instacart',
                                                         user='mysql2021',
                                                         password='mysql2021')
            elif (request.form['database'] == 'redshift'):
                if (request.form['dataset'] == 'instacart_normalized'):
                    connection = psycopg2.connect(host='redshift2021.cxixtqv0g2ru.us-east-2.redshift.amazonaws.com',
                                                  database='instacart_normalized',
                                                  user='redshift2021',
                                                  password='Redshift2021',
                                                  port="5439")
                elif (request.form['dataset'] == 'instacart'):
                    connection = psycopg2.connect(host='redshift2021.cxixtqv0g2ru.us-east-2.redshift.amazonaws.com',
                                                  database='instacart',
                                                  user='redshift2021',
                                                  password='Redshift2021',
                                                  port="5439")
            cursor = connection.cursor()
            query = request.form['query']
            init_time = datetime.datetime.now()
            cursor.execute(query)
            end_time = datetime.datetime.now()

            if (query[0:6].lower() == 'select' or query[0:4].lower() == 'show'):
                data = cursor.fetchall()
                attributes = []
                description = cursor.description
                for i in description:
                    attributes.append(i[0])
                text = 'Number of records: ' + str(cursor.rowcount)
                #cursor.close()
                #connection.close()
                #end_time = datetime.datetime.now()
                #time_elapsed = end_time - init_time
                #query = query.replace('\r\n', '?')
                #return render_template('index.html', data=results, attributes=attributes, num=num, time=time_elapsed, selection=request.form, input_query=query)
            else:
                connection.commit()
                attributes = ['Query', 'Execution result']
                data = [[query, 'Finished']]
                text = 'Number of records: 1'

            cursor.close()
            connection.close()
            time_elapsed = end_time - init_time
            query = query.replace('\r\n', '?')
            
            return render_template('index.html', data=data, attributes=attributes, text=text, time=time_elapsed, selection=request.form, input_query=query)
                #return '<h1><br>Executed query: {Done}</br><br>Time Elapsed: {time}</br></h1>'.format(Done=query,time=time_elapsed)
    
    except Exception as e:
        query = request.form['query'].replace('\r\n', '?')
        return render_template('index.html', data=[[request.form['query'], 'Failed', e]], attributes=['Query', 'Execution result', 'Error message'], text='Number of records: 1', time='NA', selection=request.form, input_query=query)
        #return '<h1>{error}</h1>'.format(error=e)

    return render_template('index.html')


if __name__ == '__main__':
    application.run(debug=True)