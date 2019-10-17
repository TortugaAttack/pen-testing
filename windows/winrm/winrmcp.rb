require 'winrm-fs'


if ARGV.length < 6
	STDOUT.print "winrmcp URL USER PASSWORD [-d|-u] FILES* folder\n"
end

connection = WinRM::Connection.new(
  endpoint: 'http://'+ARGV[0]+':5985/wsman',
  user: ARGV[1],
  password: ARGV[2]
)

file_manager = WinRM::FS::FileManager.new(connection)

# upload file.txt from the current working directory
files = []

if (ARGV[3] <=> "-u") ==0
	file_manager.create_dir(ARGV[ARGV.length-1])
end

ARGV.each_with_index do |arg, index|
  #Pr��fe, ob eine Option angegeben wurde, und wenn ja, nehme ��nderungen vor
  if index > 3 && index < ARGV.length-1
    STDOUT.print (index-4).to_s+": "+ARGV[index]+"\n"
    if (ARGV[3] <=> "-u") ==0
       file_manager.upload(ARGV[index], ARGV[ARGV.length-1])	
    end
    if (ARGV[3] <=> "-d") == 0
  	file_manager.download(ARGV[index], ARGV[ARGV.length-1])
    end
  end
end


