mv adlists.list adlists.bak
touch adlists.list
curl https://v.firebog.net/hosts/lists.php?type=nocross 2>/dev/null >> adlists.list
curl https://v.firebog.net/hosts/lists.php?type=tick 2>/dev/null >> adlists.list
echo 'https://phishing.army/download/phishing_army_blocklist.txt' >> adlists.list
pihole -g
