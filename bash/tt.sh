# find diff day from today to given date

# file to parse tt events
TT_FILE=~/tt.txt

# sample content of tt.txt:
# ** begin file tt.txt **
# 3/5/2018 event A
# 5/5/2018 event B
#
# ** end of file tt.txt **

TEXT_EDITOR=subl

# width and characters for the progress bars
# feel free to configure these
MIN_DAYS=100
MAX_OVERDUE=5

# set event's color to `WARNING_COLOR`
# when days left is less than threshold
WARNING_THRESHOLD=10
WARNING_COLOR='\033[0;33m' # orange

GREEN='\033[0;32m'
RED='\033[0;31m'
CYAN='\033[0;36m'
EVENT_DATE_COLOR=$CYAN
NC='\033[0;0m' # no color

width=28
fill_char="█"
empty_char="░"

# round function
round() { printf %.0f "$1"; }

# progress bar display function
progress() {
	progress=$1
	progress_int=${progress%.*}
    filled=$(round $(echo "$progress * $width / 100" | bc -l))

    empty=$((width - filled))
    if [ "$empty" -gt $width ]; then
    	filled=1
    	empty=$((width-1))
    fi

    # adjust overdue progress
    if [ "$progress_int" -gt 100 ]; then
    	empty=0
    	filled=$((width))
    fi

    # uncomment to debug
    # echo "width: $width, progress: $progress, filled: $filled, empty: $empty"

    # repeat the characters using printf
    printf "$fill_char%0.s" $(seq $filled)

    if [ "$empty" != 0 ]; then
    	printf "$empty_char%0.s" $(seq $((empty+1)))

    # adjust additional empty char if progress is not completed
    elif [ "$progress_int" -lt 100 ]; then
    	printf "$empty_char"

    # adjust fill char if progress is overdue
    elif [ "$progress_int" -gt 100 ]; then
    	printf "$fill_char%0.s" $(seq 1)
	fi
}

days_left() {
	now=$(date +%s)

	# format: `30/5/2018 <additional string>`
	event=$1
	due_date=$(echo $event | awk '{ print $1}')
	due_epoch=$(date -j -f '%d/%m/%Y' "$due_date" +'%s')

	event_name=$(echo $event | awk '{$1=""; print}')
	event_date=$(date -r "$due_epoch" +'%b %d')
	event_year=$(date -r "$due_epoch" +'%Y')

	if [ "$event_year" != $(date +'%Y') ]; then
		event_date=$(date -r "$due_epoch" +'%b %d, %Y')
	fi

	day_diff=$(echo "($due_epoch-$now) / (60*60*24)" | bc -l)
	due_progress=$(
		echo "100 - $day_diff" | bc -l
	)

	day_diff_int=${day_diff%.*}

	if [ "$day_diff_int" -le 0 ]; then
		if [ "$day_diff_int" -ge $((MAX_OVERDUE * -1)) ]; then
			day_diff=$((day_diff * -1))
			echo "${EVENT_DATE_COLOR}${event_date}${NC} ·${event_name}"
			echo "$(progress $due_progress) ${RED}$(round $day_diff)d ago $NC"
		fi
	else
		if [ "$day_diff_int" -le $WARNING_THRESHOLD ]; then
				echo "${EVENT_DATE_COLOR}${event_date}${NC} ·${event_name}"
				echo "$(progress $due_progress) ${WARNING_COLOR}$(round $day_diff)d left $NC"
		else
			# display progress
			echo "${EVENT_DATE_COLOR}${event_date}${NC} ·${event_name}"
			echo "$(progress $due_progress) $(round $day_diff)d left"
		fi
	fi
}

# TODO:
# - add arg `tt add <event>`
tt() {
	if [ -z "$1" ]; then
		while IFS= read -r line || [ -n "$line" ]; do
			# skip comments and empty line
			if [[ ${line:0:1} != "#" ]] && [[ ${line:0:1} != "" ]]; then
			  days_left $line
			fi
		done < $TT_FILE
	elif [[ "$1" == "file" ]]; then
		echo $TT_FILE
	elif [[ "$1" == "edit" ]] || [[ "$1" == "add" ]]; then
		$TEXT_EDITOR $TT_FILE
	elif [[ "$1" == "cat" ]]; then
		cat $TT_FILE
	else
		days_left $*
	fi
}
