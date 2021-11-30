from flask import Flask, render_template, request
import mysql.connector
import psycopg2
import datetime
from pydrill.client import PyDrill

application = Flask(__name__)

@application.route("/", methods=['GET', 'POST'])
def home_page():
    try:
        if (request.method == 'POST'): 

            database = request.form['database']
            dataset = request.form['dataset']
            
            if (database == 'mongodb'):
                drill = PyDrill(host='localhost', port=8047)
                query = request.form['query']
                init_time = datetime.datetime.now()
                result = drill.query(query, timeout=60)
                end_time = datetime.datetime.now()
                table_head = []
                for i in result.columns:
                    table_head.append(i)
                table_data = []
                for i in result.rows:
                    table_data.append(list(i.values()))
                time = end_time - init_time
                num = 'Number of records: ' + str(len(result.rows))
                query = query.replace('\r\n', '?')

            else:

                if (database == 'mysql'):
                    if (dataset == 'adnimerge'):
                        connection = mysql.connector.connect(host='mysql2021.c7wtal8gxuuf.us-east-2.rds.amazonaws.com',
                                                             database='adnimerge',
                                                             user='mysql2021',
                                                             password='mysql2021')
                    elif (dataset == 'instacart_normalized'):
                        connection = mysql.connector.connect(host='mysql2021.c7wtal8gxuuf.us-east-2.rds.amazonaws.com',
                                                             database='instacart_normalized',
                                                             user='mysql2021',
                                                             password='mysql2021')
                    elif (dataset == 'instacart'):
                        connection = mysql.connector.connect(host='mysql2021.c7wtal8gxuuf.us-east-2.rds.amazonaws.com',
                                                             database='instacart',
                                                             user='mysql2021',
                                                             password='mysql2021')
                elif (database == 'redshift'):
                    if (dataset == 'adnimerge'):
                        connection = psycopg2.connect(host='redshift2021.cxixtqv0g2ru.us-east-2.redshift.amazonaws.com',
                                                      database='adnimerge',
                                                      user='redshift2021',
                                                      password='Redshift2021',
                                                      port="5439")
                    elif (dataset == 'instacart_normalized'):
                        connection = psycopg2.connect(host='redshift2021.cxixtqv0g2ru.us-east-2.redshift.amazonaws.com',
                                                      database='instacart_normalized',
                                                      user='redshift2021',
                                                      password='Redshift2021',
                                                      port="5439")
                    elif (dataset == 'instacart'):
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

                if (query[0:6].lower() == 'select' or query[0:4].lower() == 'show' or query[0:8].lower() == 'describe'):
                    table_head = []
                    column_name = cursor.description
                    for i in column_name:
                        table_head.append(i[0])
                    table_data = cursor.fetchall()
                    num = 'Number of records: ' + str(cursor.rowcount)
                else:
                    connection.commit()
                    table_head = ['Query', 'Execution result']
                    table_data = [[query, 'Finished']]
                    num = 'Number of records: 1'

                cursor.close()
                connection.close()
                time = end_time - init_time
                query = query.replace('\r\n', '?')
            
            return render_template('index.html', table_head=table_head, table_data=table_data, num=num, time=time, database=database, dataset=dataset, query=query)
                #return '<h1><br>Executed query: {Done}</br><br>Time Elapsed: {time}</br></h1>'.format(Done=query,time=time_elapsed)
    
    except Exception as e:
        return render_template('index.html', table_head=['Query', 'Execution result', 'Error message'], table_data=[[request.form['query'], 'Failed', e]], num='Number of records: 1', time='NA', database=request.form['database'], dataset=request.form['dataset'], query=request.form['query'].replace('\r\n', '?'))
        #return '<h1>{error}</h1>'.format(error=e)

    return render_template('index.html')


if __name__ == '__main__':
    application.run(debug=True)