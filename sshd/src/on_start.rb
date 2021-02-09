#!/usr/bin/env ruby

require 'pg'

begin
    conn = PG.connect :host=>"postgres",
                      :user=>"postgres",
                      :dbname=>"postgres"
    $stdout.puts "Comnected to database"

    rows = conn.exec "select username from users"
    count = 0
    rows.each do |row|
        if row =~ /^[a-z][-a-z0-9]*$/
            `/create_user.sh #{row}`
            count += 1
        else
            $stderr.puts "username #{row} is invalid"
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
