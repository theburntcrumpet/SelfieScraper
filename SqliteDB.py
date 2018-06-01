import sqlite3, logging, os.path
class SqliteDB:
	def __init__(self,sqliteFile="Database.db"):
		existed = os.path.isfile(sqliteFile)
		self.db = sqlite3.connect(sqliteFile)
		if not existed:
			self.CreateDatabase()

	# This is ALWAYS defined by the subclass
	def CreateDatabase(self):
		pass

	def GetIdFromTable(self,idField,fieldName,tableName,fieldValue):
		c = self.db.cursor()
		ids = c.execute("SELECT {} FROM {} WHERE {} = ?".format(idField,tableName,fieldName),(fieldValue,))
		idRow = ids.fetchone()
		if len(idRow) == 0:
			return None
		return idRow[0]


	def CheckSingleValueExistsInTable(self,tableName,fieldName,fieldValue):
		c = self.db.cursor()
		existing = c.execute("SELECT COUNT(*) FROM {} WHERE {}=?".format(tableName,fieldName), (fieldValue,))
		nExistingRow = existing.fetchone()
		if(nExistingRow[0] > 0):
			return True
		return False

	# Was going to have this insert multiple values but the way the string has to be formatted in sqlite3 doesn't allow for this dynamically
	# The alternative would be to generate the values myself but they wouldn't be sql escaped
	def InsertValuesIntoTable(self,tableName,columnList,valuesList):
		if(len(columnList) != len(valuesList)):
			logging.error("column and value list must be equilength")
			return False
		strValues = ""
		for i in valuesList:
			strValues += "?,"
		strValues = strValues[:-1]
		strQuery = "INSERT INTO {} ({}) VALUES({})".format(tableName,",".join(columnList),strValues)
		c = self.db.cursor()
		c.execute(strQuery, valuesList)
		self.db.commit()