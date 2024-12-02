if [[ -z $(git status -s) ]]
then
  echo "======== tree is clean ========"
  git checkout main && git pull origin main && git fetch && git branch --merged | egrep -v "(^\*|main|dev)" | xargs git branch -d
  echo "I am done... :)"
  git branch
  exit
else
  echo "======== tree is dirty, please commit changes before running this ========"
  git status
  exit
fi
