#!/usr/bin/env cabal
{- cabal:
       build-depends: base ^>=4.14.3.0
-}

module Main where

main :: IO ()
main = do
    contents <- getContents
    putStrLn $ "Part 1: " ++ (show $ part1 contents) ++ " Part 2: " ++ (show $ part2 contents)

processInput :: String -> [Int]
processInput x = map (read::String -> Int) $ lines x

isIncreased :: (Int, Int) -> Int
isIncreased (x, y) = if (y > x) 
                        then 1
                        else 0

createTripletsSum :: [Int] -> [Int]
createTripletsSum (x:y:ls) = map (\(x,y,z) -> x + y + z) $ zip3 (x:y:ls) (y:ls) ls
createTripletsSum _ = []

part1 :: String -> Int
part1 xs = sum $ map isIncreased $ zip <*> tail $ processInput xs

part2 :: String -> Int
part2 xs = sum $ map isIncreased $ zip <*> tail $ createTripletsSum $ processInput xs