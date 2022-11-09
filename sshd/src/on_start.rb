#!/usr/bin/env ruby

require 'pg'

begin
    conn = PG.connect :host=>"postgres-service.default.svc.cluster.local",
                      :user=>"postgres",
                      :dbname=>"django"
    $stdout.puts "Comnected to database"

    rows = conn.exec "select username from auth_user"
    count = 0
    rows.each do |row|
        username = row["username"]
        if username =~ /^[a-z][-a-z0-9]*$/
            `/create_user.sh #{username}`
            count += 1
        else
            $stderr.puts "username #{username} is invalid"
            $stderr.flush
        end
    end
    if count > 0
        $stdout.puts "Synced #{count} users"
    else
        $stdout.puts "No users to sync"
    end

    $stdout.flush
ensure
    conn.close if conn
end

exec "tail -f /dev/null"
