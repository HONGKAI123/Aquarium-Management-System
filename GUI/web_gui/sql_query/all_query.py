# SJSU CMPE 138 Spring 2022 TEAM6
from mysql import connector
import time


class dbHelper():
    def timedeltaTOstr(self):
        pass


class query():
    def cursor(self, username: str = 'root', pwd: str = "lucifer"):
        self.conn = connector.connect(
            host = 'localhost',
            user = username,
            password = "qweqwe123",
            database = 'aquarium')
        return self.conn.cursor()

    def disconnect(self):
        self.cursor().close()
        self.conn.disconnect()


class aquarist():
    def __init__(self):
        self.q = query()
        self.cursor = self.q.cursor()

    # check maintanence times
    # arg = [user_id]
    def check_maint_times(self, *arg):
        """
        input: string: user_id
        :return list of column name, queryset
        """

        query = "SELECT name AS 'Facility', fa_id AS 'ID', maint_time AS 'Maintenance Time' FROM facility_maint \
        LEFT JOIN facility ON facility.fa_id = facility_maint.facility \
        LEFT JOIN maintain ON fa_id = maintain.facility \
        WHERE maint_status = FALSE \
        AND staff = '" + arg[0] + "' \
        ORDER BY maint_time ASC;"
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            self.q.disconnect()

        except connector.Error as e:
            result = e
        finally:
            return ['Facility', 'ID', 'Maintenance Time'], result

    def maintain_facility(self, *arg):
        # todo effected row not return
        """
        Update facility maintanence status
        :param arg:
        [user_id, fa_id, maint_time]
        user_id string :'987153744'
        fac_id string : '300001'
        time_slot type??? : '12:00:00'
        :return:
        """
        # Check if the fa_id and maint_time combo exists for current user
        input_match = False
        for i in self.check_maint_times(arg[0])[1]:
            if str(i[1]) == str(arg[1]) and str(i[2]) == str(arg[2]):
                input_match = True

        try:
            if input_match == True:
                query = "UPDATE facility_maint \
                SET maint_status = 1 \
                WHERE facility = '{0}' \
                AND maint_time = '{1}';".format(arg[1], arg[2])
            cursor = self.cursor()
            cursor.execute(query)

            # print(self.cursor.rowcount)
            print(query)
            print('?')
            self.q.conn.commit()
            self.q.disconnect()
        except connector.Error as e:
            print(e)

        # SJSU CMPE 138 Spring 2022 TEAM6
        finally:
            return True if self.cursor.rowcount > 0 else False


class director():
    # view events report
    def view_event(self,*arg):  # type,start_date,end_date
        """
        View events by selecting
        :param args: type (enum),start_date(str),end_date(str)

        :return: array of selected event detail
        """
        # call db connection API
        q = query()

        # sql query that reterive event detail
        sql_query = "select ev_ID, title, type, date, attendance \
                    from event join event_instance on event.ev_ID = event_instance.event \
                    where type ='{type}' and (date between '{start_date}' and '{end_date}')\
                    order by attendance desc;".format(type = arg[0], start_date = arg[1], end_date = arg[2])

        with q.cursor(username = 'root', pwd = 'root') as cur:
            cur.execute(sql_query)
            # catch return result
            res = cur.fetchall()

        return ['ev_ID', 'title', 'type', 'date', 'attend'], res


    # create new event
    def create_event(self,*arg):  # ev_ID,title,type,overseer
        """
        Create new event by inserting
        :param args: ev_ID(char-6), title(str),type(enum),overseer(char-9)

        :return: has created event into database
        """
        # call db connection API
        q = query()

        # sql query that create new event to db
        sql_query = "insert into event values ('{ev_ID}', '{title}', '{type}', null, '{overseer}');" \
            .format(ev_ID = arg[0], title = arg[1], type = arg[2], overseer = arg[3])

        with q.cursor() as cur:
            cur.execute(sql_query)

            # submit change to database
            q.conn.commit()

            # catch return result
            res = cur.rowcount

        return True if res > 0 else False


    # view staff report
    def view_staff_report(self):
        """
        :param args: N/A

        :return: array of selected report on curator-animal,
        event manager-event, aquraist-facility, aquraist-event
        """

        q = query()

        with q.cursor() as cur:
            column = []
            finalResult = []  # an array that store colunm name, report title and staff detail without formating
            for i in range(4):  # each round append one type of staff's detail
                if (i == 0):
                    sql_query = "select curator.name, animal.name\
                        from curator join animal on curator.st_ID=animal.curator;"
                    cur.execute(sql_query)
                    res = cur.fetchall()
                    column_title = ['Curator', 'Animal']  # assign column name to str variable
                    column.extend(column_title)  # insert column name
                    print(res,"0")
                    finalResult.extend(res)  # follow by staff detail

                elif (i == 1):
                    sql_query = "select event_manager.name as mangaer_Name, event.title as event_title\
                    from event_manager join event on event_manager.st_ID = event.overseer;"
                    cur.execute(sql_query)
                    column_title = ['Manager', 'Event']
                    res = cur.fetchall()
                    column.extend(column_title)
                    print(res,"1")
                    finalResult.extend(res)

                elif (i == 2):
                    sql_query = "select aquarist.name as aquarist_Name, facility.name as facility_Name\
                    from aquarist, facility, maintain\
                    where aquarist.st_ID=maintain.staff and maintain.facility = facility.fa_ID;"
                    cur.execute(sql_query)
                    column_title = ['Aquarist', 'Facility']
                    res = cur.fetchall()
                    column.extend(column_title)
                    finalResult.extend(res)

                else:
                    sql_query = "select aquarist.name as aquarist_Name, event.title as event_Name\
                    from aquarist, event, work_on\
                    where aquarist.st_ID = work_on.staff and work_on.event = event.ev_ID;"
                    cur.execute(sql_query)
                    column_title = ['Aquarist', 'Event']
                    res = cur.fetchall()
                    column.extend(column_title)
                    finalResult.extend(res)

        return column,finalResult


    # Hire Staff
    def hire_staff(self,*arg):  # role,st_ID,name,phone,email
        """
        :param args: role{aquirst,curator,event_manger}, st_ID(char-9),
        name(str), phone(char-9), email(str)

        :return: has added staff to database

        """
        # call db connection API
        q = query()

        # sql query that create new staff to db
        sql_query = "insert into {role} values ('{st_ID}', NULL, '{name}', '{phone}', '{email}');" \
            .format(role = arg[0], st_ID = arg[1], name = arg[2], phone = arg[3], email = arg[4])

        with q.cursor() as cur:
            cur.execute(sql_query)

            # submit change to database
            q.conn.commit()

            # catch return result
            res = cur.rowcount

        return True if res > 0 else False


    # Checking if Curator's animals have been reassigned before firing them
    def animalAssignCheck(st_ID):
        """
        :param args: st_ID(char-9)

        :return: has an valid reassignment
        """
        # call db connection API
        q = query()

        # sql query that reterive animal and curator from db
        sql_query = "select * from animal where animal.curator={st_ID};".format(st_ID = st_ID)

        with q.cursor() as cur:
            cur.execute(sql_query)
            # catch return result
            res = cur.fetchall()

        return True if len(res) == 0 else False  # length=0 indicates reassigned all tasks


    # Checking if event manager's events have been reassigned before firing them
    def eventAssignCheck(st_ID):
        """
        :param args: st_ID(char-9)

        :return: has an valid reassignment
        """

        # call db connection API
        q = query()

        # sql query that reterive event and manager from db
        sql_query = "select * from event where event.overseer = {st_ID};".format(st_ID = st_ID)

        with q.cursor() as cur:
            cur.execute(sql_query)
            # catch return result
            res = cur.fetchall()

        return True if len(res) == 0 else False  # length=0 indicates reassigned all tasks


    # Fire Staff
    def fire_staff(st_ID):
        """
        :param args: st_ID(char-9)

        :return: has removed staff from database
        """

        staff = ['curator', 'aquarist', 'event_manager']

        # call db connection API
        q = query()

        with q.cursor() as cur:
            # since aquarist is not in either tables, both remain true
            if (self.animalAssignCheck(st_ID) == True and eventAssignCheck(st_ID) == True):
                for i in staff:  # locate the staff's role and fire
                    # sql query that delete staff from db
                    sql_query = "delete from {staff} where st_ID ='{st_ID}';".format(staff = i, st_ID = st_ID)
                    cur.execute(sql_query)

                    # submit change to database
                    q.conn.commit()

                return True
            else:
                return False


    # Refresh events/facility/animals
    def refreshAll(self):
        """
        :param args: N/A

        :return: has update requirement
        """
        q = query()

        with q.cursor() as cur:
            sql_query_maintance = "update facility_maint set facility_maint.maint_status= false;"
            cur.execute(sql_query_maintance)

            sql_query_feeding = "update animal set animal.status = 0;"
            cur.execute(sql_query_feeding)

            # create event_instance for a new day
            localtime = time.localtime(time.time())
            newdate = str(localtime[0]) + "-" + str(localtime[1]) + "-" + str(localtime[2])  # retrieve current

            sql_query_getEvent = "select event.ev_ID from event;"
            cur.execute(sql_query_getEvent)
            eventList = cur.fetchall()

            for i in eventList:
                sql_query_renewEvent = "insert into event_instance values ('{event_ID}', '{date}', null);".format(
                    event_ID = i[0], date = newdate)
                cur.execute(sql_query_renewEvent)
            # submit change to database
            q.conn.commit()

            # catch return result
            res = cur.rowcount

        return True if res > 0 else False
